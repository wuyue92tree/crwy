#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: wuyue
@contact: wuyue92tree@163.com
@software: PyCharm
@file: dupefilters.py
@create at: 2018-06-14 14:52

这一行开始写关于本文件的说明与解释
"""

import logging
import time
import datetime
import hashlib
from crwy.utils.filter.RedisSet import RedisSet
from crwy.utils.filter.RedisSortedSet import RedisSortedSet
from scrapy.dupefilters import BaseDupeFilter
from scrapy.exceptions import NotConfigured
from scrapy_redis.connection import get_redis_from_settings

logger = logging.getLogger(__name__)


class RedisRFPDupeFilter(BaseDupeFilter):
    """
    dupefilter by redis, redis connect base on scrapy-redis connect

    warning:
        config SPIDER_NAME in settings before use
    default:
        DUPEFILTER_DEBUG = False
        DUPEFILTER_DELAY_DAY = 0
    """
    logger = logger

    def __init__(self, debug=False,
                 server=None,
                 bot_name=None,
                 spider_name=None,
                 duperliter_delay_day=None,
                 do_hash=None):
        self.debug = debug
        self.logdupes = True
        self.server = server
        self.bot_name = bot_name
        self.spider_name = spider_name
        self.duperliter_delay_day = duperliter_delay_day
        self.do_hash = do_hash

    @classmethod
    def from_settings(cls, settings):
        server = get_redis_from_settings(settings)
        debug = settings.getbool('DUPEFILTER_DEBUG')
        bot_name = settings.get('BOT_NAME')
        spider_name = settings.get('SPIDER_NAME')
        duperliter_delay_day = settings.getint('DUPEFILTER_DELAY_DAY', 0)
        do_hash = settings.getbool('DUPEFILTER_DO_HASH', True)
        if not spider_name:
            raise NotConfigured('%s - "SPIDER_NAME" is not found.' %
                                cls.__name__)
        return cls(debug=debug, server=server, bot_name=bot_name,
                   spider_name=spider_name,
                   duperliter_delay_day=duperliter_delay_day,
                   do_hash=do_hash)

    def request_seen(self, request):
        if not request.meta.get('dupefilter_key', None):
            return False

        if len(request.meta.get('redirect_urls', [])) > 0:
            # skip url from redirect
            return False

        dupefilter_key = request.meta.get('dupefilter_key')
        dupefilter_key = hashlib.sha1(dupefilter_key).hexdigest() if \
            self.do_hash else dupefilter_key

        # SPIDER_NAME for dupefilter
        key = '{bot_name}:{spider_name}'.format(
            bot_name=self.bot_name,
            spider_name=self.spider_name)

        if request.meta.get('duperliter_delay_day', ''):
            self.duperliter_delay_day = int(request.meta.get(
                'duperliter_delay_day'))

        if self.duperliter_delay_day == 0:
            s = RedisSet(key, server=self.server)
            if s.sadd(dupefilter_key) is True:
                return False
            self.logger.info('Filtered dupefilter_key: %s' %
                             dupefilter_key)
            return True
        else:
            z = RedisSortedSet(key, server=self.server)
            now = time.time()
            last_time = z.zscore(dupefilter_key)

            if not last_time:
                z.zadd(now, dupefilter_key)
                return False

            if (datetime.datetime.utcfromtimestamp(now) -
                datetime.datetime.utcfromtimestamp(last_time)).days >= \
                    self.duperliter_delay_day:
                z.zadd(now, dupefilter_key)
                return False
            self.logger.info('Filtered dupefilter_key within %s day(s): %s' %
                             (self.duperliter_delay_day,
                              request.meta.get('dupefilter_key')))
            return True

    def log(self, request, spider):  # log that a request has been filtered
        if self.debug:
            msg = "Filtered duplicate request: %(request)s"
            self.logger.debug(msg, {
                'request': request.meta.get('dupefilter_key')}, extra={
                'spider': spider})
        elif self.logdupes:
            msg = ("Filtered duplicate request: %(request)s"
                   " - no more duplicates will be shown"
                   " (see DUPEFILTER_DEBUG to show all duplicates)")
            self.logger.debug(msg, {'request': request},
                              extra={'spider': spider})
            self.logdupes = False

        spider.crawler.stats.inc_value('dupefilter/filtered', spider=spider)


class ReleaseDupefilterKey(object):
    """
    rm dupefilter_key from redis, when call response
    """

    def call(self, spider, dupefilter_key):

        if not dupefilter_key:
            return

        obj = RedisRFPDupeFilter().from_settings(spider.settings)

        dupefilter_key = hashlib.sha1(dupefilter_key).hexdigest() if \
            obj.do_hash else dupefilter_key

        # SPIDER_NAME for dupefilter
        key = '{bot_name}:{spider_name}'.format(
            bot_name=obj.bot_name,
            spider_name=obj.spider_name)

        if obj.duperliter_delay_day == 0:
            s = RedisSet(key, server=obj.server)
            s.srem(dupefilter_key)
        else:
            z = RedisSortedSet(key, server=obj.server)
            z.zrem(dupefilter_key)
        obj.logger.info('dupefilter_key: {} released.'.format(
            dupefilter_key))


release_dupefilter_key = ReleaseDupefilterKey()

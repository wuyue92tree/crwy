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


class RedisRFPDupeFilter(BaseDupeFilter):
    """
    dupefilter by redis
    
    warning:
        config SPIDER_NAME in settings before use
    default:
        DUPEFILTER_REDIS_HOST = '127.0.0.1'
        DUPEFILTER_REDIS_PORT = 6379
        DUPEFILTER_REDIS_DB = 0
        DUPEFILTER_REDIS_PASSWORD = ''
        DUPEFILTER_DELAY_DAY = 0
    """

    def __init__(self, debug=False,
                 redis_host=None,
                 redis_port=None,
                 redis_db=None,
                 redis_password=None,
                 bot_name=None,
                 spider_name=None,
                 duperliter_delay_day=None,
                 do_hash=None):
        self.debug = debug
        self.logdupes = True
        self.redis_host = redis_host
        self.redis_port = redis_port
        self.redis_db = redis_db
        self.redis_password = redis_password
        self.bot_name = bot_name
        self.spider_name = spider_name
        self.duperliter_delay_day = duperliter_delay_day
        self.do_hash = do_hash
        self.logger = logging.getLogger(__name__)

    @classmethod
    def from_settings(cls, settings):
        debug = settings.getbool('DUPEFILTER_DEBUG')
        redis_host = settings.get('DUPEFILTER_REDIS_HOST', '127.0.0.1')
        redis_port = settings.get('DUPEFILTER_REDIS_PORT', 6379)
        redis_db = settings.get('DUPEFILTER_REDIS_DB', 0)
        redis_password = settings.get('DUPEFILTER_REDIS_PASSWORD', '')
        bot_name = settings.get('BOT_NAME')
        spider_name = settings.get('SPIDER_NAME')
        duperliter_delay_day = settings.getint('DUPEFILTER_DELAY_DAY', 0)
        do_hash = settings.getbool('DUPEFILTER_DO_HASH', True)
        if not spider_name:
            raise NotConfigured('%s - "SPIDER_NAME" is not found.' %
                                cls.__name__)
        return cls(debug=debug, redis_host=redis_host, redis_port=redis_port,
                   redis_db=redis_db, redis_password=redis_password,
                   bot_name=bot_name, spider_name=spider_name,
                   duperliter_delay_day=duperliter_delay_day,
                   do_hash=do_hash)

    def request_seen(self, request):
        if not request.meta.get('dupefilter_key', None):
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
            s = RedisSet(key,
                         host=self.redis_host,
                         port=self.redis_port,
                         db=self.redis_db,
                         password=self.redis_password)
            if s.sadd(dupefilter_key) is True:
                return False
            self.logger.info('Filtered dupefilter_key: %s' %
                             dupefilter_key)
            return True
        else:
            z = RedisSortedSet(key,
                               host=self.redis_host,
                               port=self.redis_port,
                               db=self.redis_db,
                               password=self.redis_password)

            now = time.time()
            last_time = z.zscore(dupefilter_key)

            if not last_time:
                z.zadd(now, dupefilter_key)
                return False

            if (datetime.datetime.utcfromtimestamp(now) -
                datetime.datetime.utcfromtimestamp(last_time)).days > \
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

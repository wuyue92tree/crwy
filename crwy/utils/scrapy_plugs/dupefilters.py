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
from crwy.utils.filter.RedisSet import RedisSet
from scrapy.dupefilters import BaseDupeFilter


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
    """
    def __init__(self, debug=False,
                 redis_host=None,
                 redis_port=None,
                 redis_db=None,
                 redis_password=None,
                 bot_name=None,
                 spider_name=None):
        self.debug = debug
        self.logdupes = True
        self.redis_host = redis_host
        self.redis_port = redis_port
        self.redis_db = redis_db
        self.redis_password = redis_password
        self.bot_name = bot_name
        self.spider_name = spider_name
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
        return cls(debug=debug, redis_host=redis_host, redis_port=redis_port,
                   redis_db=redis_db, redis_password=redis_password,
                   bot_name=bot_name, spider_name=spider_name)

    def request_seen(self, request):
        if not request.meta.get('dupefilter_key', None):
            return False

        # SPIDER_NAME for dupefilter
        key = '{bot_name}:{spider_name}'.format(
            bot_name=self.bot_name,
            spider_name=self.spider_name)

        s = RedisSet(key,
                     host=self.redis_host,
                     port=self.redis_port,
                     db=self.redis_db,
                     password=self.redis_password)
        if s.sadd(request.meta.get('dupefilter_key')) is True:
            return False
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

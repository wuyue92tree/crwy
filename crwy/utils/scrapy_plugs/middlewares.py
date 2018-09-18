#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: wuyue
@contact: wuyue92tree@163.com
@software: PyCharm
@file: middlewares.py
@create at: 2018-06-26 18:21

这一行开始写关于本文件的说明与解释
"""

import json
import random

from scrapy.downloadermiddlewares.retry import RetryMiddleware
from crwy.utils.data.RedisHash import RedisHash
from crwy.exceptions import CrwyScrapyPlugsException


class CookieMiddleware(RetryMiddleware):
    """
    cookie_pool
        eg: '{"a": 1, "b": "aaa"}'
    """

    def __init__(self, settings):
        super(CookieMiddleware, self).__init__(settings)
        self.site = settings.get('SITE', None)
        if not self.site:
            raise CrwyScrapyPlugsException('SITE_NOT_SET')

        self.h = RedisHash(
            'cookie_pool:{}'.format(self.site),
            host=settings.get('COOKIE_REDIS_HOST', '127.0.0.1'),
            port=settings.get('COOKIE_REDIS_PORT', 6379),
            password=settings.get('COOKIE_REDIS_PASSWORD', ''),
            db=settings.get('COOKIE_REDIS_DB', 0),
        )

    def process_request(self, request, spider):
        if request.meta.get('cookie_user', ''):
            user = request.meta.get('cookie_user')
        else:
            users = self.h.hkeys()
            if len(users) > 0:
                user = random.choice(users)
                if request.meta.get('keep_cookie_user', False) is True:
                    request.meta['cookie_user'] = user
            else:
                raise CrwyScrapyPlugsException(
                    'no user in cookie_pool:{}'.format(self.site))
        cookie = self.h.hget(user)
        if cookie:
            request.cookies = json.loads(cookie)
            spider.logger.debug('get_cookie_success: {}'.format(user))
        else:
            spider.logger.warning('get_cookie_failed: {}'.format(user))

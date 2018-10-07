#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: wuyue
@contact: wuyue92tree@163.com
@software: PyCharm
@file: middlewares.py
@create at: 2018-06-26 18:21

这一行开始写关于本文件的说明与解释

通过redis hash表记录站点cookie

key为 cookie_pool:SITE (SITE需要在settings中指定)
field为 账号cookie的唯一标识，可以是username，id等，具体自行约定
value为 cookie值，必须为json格式

"""

import json
import random
from scrapy.downloadermiddlewares.retry import RetryMiddleware
from scrapy_redis.connection import get_redis_from_settings
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

        self.server = get_redis_from_settings(settings)

        self.h = RedisHash(
            'cookie_pool:{}'.format(self.site),
            server=self.server
        )

    def process_request(self, request, spider):
        """
        cookie_user不为空时，获取cookie_user对应的cookie
        keep_cookie_user为True时，将设置cookie_user，并传递到子请求
        :param request:
        :param spider:
        :return:
        """
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
            # 字典存入redis，取出时未string，通过eval进行还原
            request.cookies = eval(cookie)
            spider.logger.debug('get_cookie_success: {}'.format(
                user.decode('utf-8')))
        else:
            spider.logger.warning('get_cookie_failed: {}'.format(
                user.decode('utf-8')))

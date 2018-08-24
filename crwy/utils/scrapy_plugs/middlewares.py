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

import base64
import json
import logging
import random

from six.moves.urllib.parse import unquote
from scrapy.utils.httpobj import urlparse_cached
from scrapy.utils.python import to_bytes
from scrapy.downloadermiddlewares.retry import RetryMiddleware
from crwy.utils.data.RedisHash import RedisHash
from crwy.exceptions import CrwyScrapyPlugsException

logger = logging.getLogger(__name__)


class ProxyMiddleware(object):
    def __init__(self, username=None, password=None, server=None, notice=True,
                 auth_encoding='latin-1'):
        self.username = username
        self.password = password
        self.server = server
        self.notice = notice
        self.auth_encoding = auth_encoding

    @classmethod
    def from_settings(cls, settings):
        username = settings.get('PROXY_USERNAME', None)
        password = settings.get('PROXY_PASSWORD', None)
        server = settings.get('PROXY_SERVER', None)
        notice = settings.getbool('PROXY_NOTICE', True)
        auth_encoding = settings.get('PROXY_AUTH_ENCODING', 'latin-1')
        if not server:
            raise CrwyScrapyPlugsException('PROXY_SEVER_NOT_SET')
        return cls(username=username, password=password, server=server,
                   notice=notice, auth_encoding=auth_encoding)

    def _basic_auth_header(self, username, password):
        user_pass = to_bytes(
            '%s:%s' % (unquote(username), unquote(password)),
            encoding=self.auth_encoding)
        return base64.b64encode(user_pass).strip()

    def process_request(self, request, spider):
        parsed = urlparse_cached(request)
        scheme = parsed.scheme
        auth_prefix = ''
        if not request.meta.get('proxy', ''):
            request.meta['proxy'] = scheme + '://' + self.server
        if request.meta.get('proxy_user_pass', ''):
            self.username, self.password = request.meta.get(
                'proxy_user_pass').split(':')
        if self.username and self.password:
            auth_prefix = '%s:%s@' % (self.username, self.password)
            request.headers["Proxy-Authorization"] = \
                b'Basic ' + self._basic_auth_header(
                    self.username, self.password)
        if self.notice:
            spider.logger.info(
                'Proxy setup: %s://%s%s'
                % (scheme, auth_prefix, self.server)
            )


class CookieMiddleware(RetryMiddleware):
    def __init__(self, settings):
        super(CookieMiddleware, self).__init__(settings)
        self.site = settings.get('SITE', None)
        if not self.site:
            raise CrwyScrapyPlugsException('SITE_NOT_SET')

        self.h = RedisHash('cookie_pool:{}'.format(self.site))

    def process_request(self, request, spider):
        users = self.h.hkeys()
        if len(users) > 0:
            user = random.choice(users)
            cookie = self.h.hget(user)
            if cookie:
                request.headers['Cookie'] = cookie
                print(request.headers)
                logger.debug('get_cookie_success: {}'.format(user))
            else:
                logger.warning('get_cookie_failed: {}'.format(user))
        else:
            raise CrwyScrapyPlugsException(
                'no user in cookie_pool:{}'.format(self.site))

    # def process_response(self, request, response, spider):

    # """
    # 下面的我删了，各位小伙伴可以尝试以下完成后面的工作

    # 你需要在这个位置判断cookie是否失效

    # 然后进行相应的操作，比如更新cookie  删除不能用的账号

    # 写不出也没关系，不影响程序正常使用，

    # """

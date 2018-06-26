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
from six.moves.urllib.parse import unquote
from scrapy.utils.httpobj import urlparse_cached
from scrapy.exceptions import NotConfigured
from scrapy.utils.python import to_bytes


class AbyProxyMiddleware(object):
    def __init__(self, username=None, password=None, server=None,
                 auth_encoding='utf-8'):
        self.username = username
        self.password = password
        self.server = server
        self.auth_encoding = auth_encoding

    def _basic_auth_header(self, username, password):
        user_pass = to_bytes(
            '%s:%s' % (unquote(username), unquote(password)),
            encoding=self.auth_encoding)
        return base64.b64encode(user_pass).strip()

    @classmethod
    def from_settings(cls, settings):
        username = settings.get('ABY_PROXY_USERNAME', None)
        password = settings.get('ABY_PROXY_PASSWORD', None)
        server = settings.get('ABY_PROXY_SERVER', None)
        auth_encoding = settings.get('ABY_AUTH_ENCODING', 'utf-8')
        if not username or not password or not server:
            raise NotConfigured('ABY_PROXY_CONFIG_NOT_ENOUGH')
        return cls(username=username, password=password, server=server,
                   auth_encoding=auth_encoding)

    def process_request(self, request, spider):
        parsed = urlparse_cached(request)
        scheme = parsed.scheme
        request.meta["proxy"] = scheme + '://' + self.server
        request.headers["Proxy-Authorization"] = \
            b'Basic ' + self._basic_auth_header(self.username, self.password)
        spider.logger.info('Aby proxy setup: %s | %s'
                           % (self.username, self.password))

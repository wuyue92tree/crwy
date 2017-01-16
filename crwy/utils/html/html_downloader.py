#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: wuyue92tree@163.com

import random
import pycurl
import urllib
import certifi

try:
    from io import BytesIO
except ImportError:
    from StringIO import StringIO as BytesIO


class HtmlDownloader(object):
    def download(self, url, method='GET', postdata=None, proxy=None, proxy_userpwd=None, cookie=None, cookiefile=None, cookiejar=None, Gzip=False, debug=False, autoclose=True, useragent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:46.0) Gecko/20100101 Firefox/46.0', referer='http://spider.wuyue.tk', FOLLOWLOCATION=1, MAXREDIRS=5, TIMEOUT=600):
        self.c = pycurl.Curl()
        self.c.setopt(pycurl.USERAGENT, useragent)
        self.c.setopt(pycurl.REFERER, referer)
        self.c.setopt(pycurl.HTTPHEADER, ['text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'])
        self.buffer = BytesIO()
        self.header = BytesIO()

        if debug:
            self.c.setopt(self.c.VERBOSE, 1)

        self.c.setopt(self.c.URL, url)
        # 设置最大重定向次数
        self.c.setopt(self.c.FOLLOWLOCATION, FOLLOWLOCATION)
        # 设置最大refer次数
        self.c.setopt(pycurl.MAXREDIRS, MAXREDIRS)
        # 设置超时时间
        self.c.setopt(pycurl.TIMEOUT, TIMEOUT)
        # 将结果写入buffer中
        self.c.setopt(self.c.WRITEDATA, self.buffer)
        # 获取header信息
        self.c.setopt(pycurl.HEADERFUNCTION, self.header.write)

        self.c.setopt(pycurl.CAINFO, certifi.where())

        self.c.setopt(pycurl.ENCODING, 'gzip, deflate, sdch')

        if proxy:
            ip = 'http://' + str(random.sample(proxy, 1)[0].encode('utf-8'))
            self.c.setopt(self.c.PROXY, ip)

        if proxy_userpwd:
            self.c.setopt(pycurl.PROXYUSERPWD, proxy_userpwd)

        if cookie:
            self.c.setopt(pycurl.COOKIE, cookie)

        if cookiefile:
            self.c.setopt(pycurl.COOKIEFILE, cookiefile)

        if cookiejar:
            self.c.setopt(pycurl.COOKIEJAR, cookiejar)

        if method == 'POST':
            self.c.setopt(pycurl.POST, 1)
            self.c.setopt(pycurl.POSTFIELDS, urllib.urlencode(postdata))

        self.c.perform()

        if self.get_response_code() != 200:
            return

        res = self.buffer.getvalue()

        if autoclose:
            self.c.close()
            self.buffer.close()
            self.header.close()

        return res

    def get_header(self):
        return self.header.getvalue()

    def get_http_conn_time(self):
        return self.c.getinfo(pycurl.CONNECT_TIME)

    def get_http_total_time(self):
        return self.c.getinfo(pycurl.TOTAL_TIME)

    def get_response_code(self):
        return self.c.getinfo(pycurl.RESPONSE_CODE)

    def close(self):
        self.c.close()
        self.buffer.close()
        self.header.close()

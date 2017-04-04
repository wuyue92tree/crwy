#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: wuyue92tree@163.com

from gevent import monkey
monkey.patch_all()
import random
import urllib
import certifi
import geventcurl as pycurl

try:
    from io import BytesIO
except ImportError:
    from StringIO import StringIO as BytesIO


class Response(object):
    def __init__(self):
        self.method = None
        self.content = None
        self.code = None
        self.header = None
        self.http_conn_time = None
        self.http_total_time = None
        self.proxy = None
        self.proxy_userpwd = None
        self.useragent = None
        self.cookie = None
        self.refer = None
        self.post_data = None

    def __repr__(self):
        return self.content


class HtmlDownloader(object):
    def download(self, url, method='GET', postdata=None, proxy=None, proxy_userpwd=None, cookie=None, cookiefile=None, cookiejar=None, debug=False, autoclose=True, useragent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:46.0) Gecko/20100101 Firefox/46.0', referer='http://spider.wuyue.tk', FOLLOWLOCATION=1, MAXREDIRS=5, TIMEOUT=600):
        c = pycurl.Curl()
        response = Response()
        c.setopt(pycurl.USERAGENT, useragent)
        c.setopt(pycurl.REFERER, referer)
        c.setopt(pycurl.HTTPHEADER, ['text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'])
        buffer = BytesIO()
        header = BytesIO()

        if debug:
            c.setopt(c.VERBOSE, 1)

        c.setopt(c.URL, url)
        # 设置最大重定向次数
        c.setopt(c.FOLLOWLOCATION, FOLLOWLOCATION)
        # # 设置最大refer次数
        c.setopt(pycurl.MAXREDIRS, MAXREDIRS)
        # # 设置超时时间
        c.setopt(pycurl.TIMEOUT, TIMEOUT)
        # 将结果写入buffer中
        c.setopt(pycurl.WRITEFUNCTION, buffer.write)
        # 获取header信息
        c.setopt(pycurl.HEADERFUNCTION, header.write)

        c.setopt(pycurl.CAINFO, certifi.where())

        c.setopt(pycurl.ENCODING, 'gzip, deflate, sdch')

        if proxy:
            ip = 'http://' + str(random.sample(proxy, 1)[0].encode('utf-8'))
            c.setopt(c.PROXY, ip)
            response.proxy = ip

        if proxy_userpwd:
            c.setopt(pycurl.PROXYUSERPWD, proxy_userpwd)
            response.proxy_userpwd = proxy_userpwd

        if cookie:
            c.setopt(pycurl.COOKIE, cookie)

        if cookiefile:
            c.setopt(pycurl.COOKIEFILE, cookiefile)

        if cookiejar:
            c.setopt(pycurl.COOKIEJAR, cookiejar)

        if method == 'POST':
            c.setopt(pycurl.POST, 1)
            c.setopt(pycurl.POSTFIELDS, urllib.urlencode(postdata))
            response.post_data = postdata

        c.perform()

        # 将请求结果写入Response()

        response.method = method
        response.content = buffer.getvalue()
        response.code = c.getinfo(pycurl.RESPONSE_CODE)
        response.header = header.getvalue()
        response.http_conn_time = c.getinfo(pycurl.CONNECT_TIME)
        response.http_total_time = c.getinfo(pycurl.TOTAL_TIME)
        response.useragent = useragent
        response.refer = referer
        response.cookie = cookie

        buffer.close()
        header.close()

        if autoclose:
            c.close()

            return response

        return c, response

    def close(self, c):
        c.close()


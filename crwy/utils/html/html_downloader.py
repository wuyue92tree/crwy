# -*- coding: utf-8 -*-
# import urllib2
import zlib
import random
import pycurl
try:
    from io import BytesIO
except ImportError:
    from StringIO import StringIO as BytesIO


class HtmlDownloader(object):
    def download(self, url, Gzip=False, Proxy=None, Cookie=None):
        if url is None:
            return None

        headers = [
            'User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:46.0) Gecko/20100101 Firefox/46.0',
            'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language: zh-cn,zh;q=0.8,en-us;q=0.5,en;q=0.3',
            # 'Accept-Encoding: gzip, deflate',
            'Connection: keep-alive',
            'Referer: http://spider.baifendian.com',
            'Cookie: %s' % Cookie
        ]

        if Gzip:
            headers.append('Accept-Encoding: gzip, deflate')

        c = pycurl.Curl()
        buffer = BytesIO()

        # self.c.setopt(c.VERBOSE, True)
        c.setopt(c.URL, url)
        # 设置最大refer次数
        c.setopt(pycurl.MAXREDIRS, 5)

        if Proxy is not None:
            proxy = 'http://' + str(random.sample(Proxy, 1)[0][0].encode('utf-8'))
            c.setopt(c.PROXY, proxy)

        c.setopt(c.HTTPHEADER, headers)
        c.setopt(c.WRITEDATA, buffer)
        c.perform()
        c.close()

        res = buffer.getvalue()

        if Gzip:
            res = zlib.decompress(res, 16 + zlib.MAX_WBITS)

        return res

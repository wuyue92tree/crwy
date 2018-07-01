#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: wuyue
@contact: wuyue92tree@163.com
@software: PyCharm
@file: chaojiying.py
@create at: 2018-05-11 16:33

这一行开始写关于本文件的说明与解释
"""

import requests
from hashlib import md5


class ChaoJiYingApi(object):
    def __init__(self, username, password, soft_id):
        self.username = username
        self.password = md5(password).hexdigest()
        self.soft_id = soft_id
        self.base_params = {
            'user': self.username,
            'pass2': self.password,
            'softid': self.soft_id,
        }
        self.headers = {
            'Connection': 'Keep-Alive',
            'User-Agent': 'Mozilla/4.0 (compatible; MSIE 8.0;'
                          ' Windows NT 5.1; Trident/4.0)',
        }

    def post_pic(self, im, code_type):
        """
        im: 图片字节
        codetype: 题目类型 参考 http://www.chaojiying.com/price.html
        """
        params = {
            'codetype': code_type,
        }
        params.update(self.base_params)
        files = {'userfile': ('ccc.jpg', im)}
        r = requests.post('http://upload.chaojiying.net/Upload/Processing.php',
                          data=params, files=files, headers=self.headers)
        return r.json()

    def report_error(self, im_id):
        """
        im_id:报错题目的图片ID
        """
        params = {
            'id': im_id,
        }
        params.update(self.base_params)
        r = requests.post(
            'http://upload.chaojiying.net/Upload/ReportError.php', data=params,
            headers=self.headers)
        return r.json()

    def decode(self, img_path, code_type):
        im = open(img_path, 'rb').read()
        res = self.post_pic(im, code_type)
        # {u'err_str': u'OK', u'err_no': 0,
        #  u'md5': u'a11171f1f444e8d1992926f4ca16c7d8',
        #  u'pic_id': u'6031116291508600001',
        #  u'pic_str': u'113,72|220,81|138,101'}
        if res.get('err_no') == 0 and res.get('err_str') == u'OK':
            return res.get('pic_str')
        return

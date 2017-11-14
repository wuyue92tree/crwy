#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: wuyue
@contact: wuyue@mofanghr.com
@software: PyCharm
@file: tianma168.py
@create at: 2017-10-27 09:57

这一行开始写关于本文件的说明与解释
"""

from __future__ import print_function

import traceback
from crwy.spider import Spider


class TianMa168(Spider):
    def __init__(self, username, password, item_id):
        super(TianMa168, self).__init__()
        if username and password and item_id:
            self.username = username
            self.password = password
            self.item_id = item_id
        else:
            print("[TianMa168] 参数不足.")
            exit()

    def login(self):
        """
        TianMa168 登录
        :return: 登录token&账户余额&最大登录客户端个数&最多获取号码数&单个客户端最多获取号码数&折扣
        """

        try:
            url = "http://api.tianma168.com/tm/Login?uName=%s&pWord" \
                  "=%s&Developer=" % (self.username, self.password)
            res = self.html_downloader.download(url)

            if res.content is None:
                print("[TianMa168] 登录失败.")
                return

            res_lst = res.content.strip().split("&")

            # ['Gsmrjv6sgENiAVsXH2fpzBG8BkKFkbA66A120833',
            # '103.6020', '500', '800', '500', '0.99', '0.0000']
            # print(res.content)
            return res_lst
        except Exception as e:
            traceback.print_exc(e)
            return

    def get_phone(self, token, count=1, area='', phone_type=0,
                  phone='', not_prefix=''):
        """
        获取手机号
        :param token:   登录token
        :param count:	获取数量 [不填默认1个]
        :param area:    区域 [不填则 随机]
        :param phone_type:  运营商 [不填为 0] 0 [随机] 1 [移动] 2 [联通] 3 [电信] 4 [虚拟] 5 [非虚拟]
        :param phone:   指定号码
        :param not_prefix:  不要号段 (例子:notPrefix=170|177 ,代表不获取170和177的号段)
        :return: 13112345678;13698763743;13928370932;
        """
        try:
            url = "http://api.tianma168.com/tm/getPhone?ItemId=%s&token" \
                  "=%s&Count=%s&Area=%s&PhoneType=%s&Phone=%s&notPrefix=%s" \
                  % (self.item_id, token, count, area, phone_type, phone,
                     not_prefix)

            res = self.html_downloader.download(url)
            if not res.content:
                print("[TianMa168] 获取手机号失败.")
                return
            # print(res.content)
            return res.content.strip().split(';')[:-1]

        except Exception as e:
            traceback.print_exc(e)
            return

    def get_message(self, token, phone):
        """
        获取短信消息
        :param token:   登录token
        :param phone:   手机号
        :return:
        """
        try:
            url = "http://api.tianma168.com/tm/getMessage?token=%s&itemId" \
                  "=%s&phone=%s" % (token, self.item_id, phone)
            res = self.html_downloader.download(url)

            if 'False' in res.content:
                print("[TianMa168] 获取短信失败.")
                return

            else:
                print(res.text.encode('utf-8'))
                return res.text

        except Exception as e:
            traceback.print_exc(e)
            return

    def release_phone(self, token, phone):
        try:
            url = "http://api.tianma168.com/tm/releasePhone?token" \
                  "=%s&phoneList=%s-%s;" % (token, phone, self.item_id)
            res = self.html_downloader.download(url)

            if phone in res.content:
                print("[TianMa168] 手机号释放成功.")
                return res.content

            else:
                print("[TianMa168] 手机号释放失败.")
                return

        except Exception as e:
            traceback.print_exc(e)
            return

    def add_black(self, token, phone):
        try:
            url = "http://api.tianma168.com/tm/addBlack?token" \
                  "=%s&phoneList=%s-%s;" % (token, self.item_id, phone)
            res = self.html_downloader.download(url)

            print(res.content)
            if 'Ok' in res.content:
                print("[TianMa168] 手机号拉黑成功.")
                return res.content

            else:
                print("[TianMa168] 手机号拉黑失败.")
                return

        except Exception as e:
            traceback.print_exc(e)
            return

#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: wuyue
@contact: wuyue92tree@163.com
@software: PyCharm
@file: yima.py
@create at: 2017-10-27 09:57

这一行开始写关于本文件的说明与解释
"""

from __future__ import print_function, unicode_literals

from crwy.spider import Spider
from crwy.exceptions import CrwyException


class YiMa(Spider):
    def __init__(self, username, password, item_id):
        super(YiMa, self).__init__()
        if username and password and item_id:
            self.username = username
            self.password = password
            self.item_id = item_id
        else:
            raise CrwyException("[YiMa] params not valid.")

    def login(self):
        """
        YiMa 登录
        :return: 登录token
        """

        try:
            url = "http://api.fxhyd.cn/UserInterface.aspx?" \
                  "action=login&username={username}" \
                  "&password={password}".format(username=self.username,
                                                password=self.password)
            res = self.html_downloader.download(url)

            if 'success' not in res.text:
                raise CrwyException("[YiMa] Login failed.")

            return res.text.strip().split("|")[-1]
        except Exception as e:
            raise CrwyException(e)

    def get_phone(self, token, phone_type='',
                  phone='', not_prefix=''):
        """
        获取手机号
        :param token:   登录token
        :param phone_type:  运营商 1 [移动] 2 [联通] 3 [电信]
        :param phone:   指定号码
        :param not_prefix:  不要号段 (例子:notPrefix=170.177 ,代表不获取170和177的号段)
        :return: 手机号码
        """
        try:
            url = "http://api.fxhyd.cn/UserInterface.aspx?action=getmobile&" \
                  "token={token}&itemid={item_id}&excludeno=" \
                  "{not_prefix}&isp={phone_type}&" \
                  "mobile={phone}".format(token=token, item_id=self.item_id,
                                          not_prefix=not_prefix,
                                          phone_type=phone_type, phone=phone)

            res = self.html_downloader.download(url)
            if 'success' not in res.text:
                raise CrwyException("[YiMa] get phone failed.")

            # print(res.text)
            return res.text.strip().split('|')[-1]

        except Exception as e:
            raise CrwyException(e)

    def get_message(self, token, phone):
        """
        获取短信消息
        :param token:   登录token
        :param phone:   手机号
        :return:
        """
        try:
            url = "http://api.fxhyd.cn/UserInterface.aspx?action=getsms&" \
                  "token={token}&itemid={item_id}&mobile={phone}" \
                  "&release=0".format(token=token, item_id=self.item_id,
                                      phone=phone)
            res = self.html_downloader.download(url)

            if 'success' not in res.text:
                raise CrwyException("[YiMa] get message failed.")

            else:
                return res.text.strip().split('|')[-1]

        except Exception as e:
            raise CrwyException(e)

    def release_phone(self, token, phone):
        try:
            url = "http://api.fxhyd.cn/UserInterface.aspx?action=release&" \
                  "token={token}&itemid={item_id}&mobile={phone}" \
                  "&release=0".format(token=token, item_id=self.item_id,
                                      phone=phone)
            res = self.html_downloader.download(url)

            if 'success' not in res.text:
                raise CrwyException("[YiMa] release phone failed.")

        except Exception as e:
            raise CrwyException(e)

    def add_black(self, token, phone):
        try:
            url = "http://api.fxhyd.cn/UserInterface.aspx?action=addignore&" \
                  "token={token}&itemid={item_id}&mobile={phone}" \
                  "&release=0".format(token=token, item_id=self.item_id,
                                      phone=phone)
            res = self.html_downloader.download(url)

            if 'success' not in res.text:
                raise CrwyException("[YiMa] black phone failed.")

        except Exception as e:
            raise CrwyException(e)

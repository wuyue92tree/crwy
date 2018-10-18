#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: wuyue
@contact: wuyue92tree@163.com
@software: IntelliJ IDEA
@file: xunma.py
@create at: 2018-09-14 11:41

这一行开始写关于本文件的说明与解释
"""


from __future__ import print_function, unicode_literals

from crwy.spider import Spider
from crwy.exceptions import CrwyExtendException


class XunMa(Spider):
    def __init__(self, username, password, item_id):
        super(XunMa, self).__init__()
        if username and password and item_id:
            self.username = username
            self.password = password
            self.item_id = item_id
        else:
            raise CrwyExtendException("[XunMa] params not valid.")

    def login(self):
        """
        XunMa 登录
        :return: 登录token
        """
        try:
            url = "http://xapi.xunma.net/Login?uName={username}" \
                  "&pWord={password}&Code=UTF8".format(username=self.username,
                                                       password=self.password)
            res = self.html_downloader.download(url)

            return res.text.strip().split("&")[0]
        except Exception as e:
            raise CrwyExtendException(e)

    def get_phone(self, token, phone_type='', phone=''):
        """
        获取手机号
        :param token:   登录token
        :param phone_type:  运营商 1 [移动] 2 [联通] 3 [电信]
        :param phone:   指定号码
        :return: 手机号码
        """
        try:
            url = "http://xapi.xunma.net/getPhone?ItemId=" \
                  "{item_id}&token={token}&" \
                  "PhoneType={phone_type}&Code=UTF8&" \
                  "Phone={phone}".format(token=token, item_id=self.item_id,
                                         phone_type=phone_type, phone=phone)

            res = self.html_downloader.download(url)
            return res.text.strip().split(';')[0]

        except Exception as e:
            raise CrwyExtendException(e)

    def get_message(self, token, phone):
        """
        获取短信消息
        :param token:   登录token
        :param phone:   手机号
        :return:
        """
        try:
            # http://xapi.xunma.net/getMessage?token=登陆token&itemId=项目ID&phone=手机号码
            url = "http://xapi.xunma.net/getMessage?" \
                  "token={token}&itemId={item_id}&phone={phone}" \
                  "&Code=UTF8".format(token=token,
                                      item_id=self.item_id, phone=phone)
            res = self.html_downloader.download(url)

            return res.text.strip().split('&')[-1]

        except Exception as e:
            raise CrwyExtendException(e)

    def release_phone(self, token, phone):
        try:
            # http://xapi.xunma.net/releasePhone?token=登陆token&phoneList=phone-itemId;phone-itemId;
            url = "http://xapi.xunma.net/releasePhone?" \
                  "token={token}&phoneList={phone};" \
                  "&Code=UTF8".format(token=token, phone=phone)
            self.html_downloader.download(url)

        except Exception as e:
            raise CrwyExtendException(e)

    def add_black(self, token, phone):
        try:
            url = "http://xapi.xunma.net/addBlack?" \
                  "token={token}&phoneList={phone};" \
                  "&Code=UTF8".format(token=token, phone=phone)
            self.html_downloader.download(url)

        except Exception as e:
            raise CrwyExtendException(e)

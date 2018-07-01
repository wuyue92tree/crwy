#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: wuyue
@contact: wuyue92tree@163.com
@software: PyCharm
@file: dingding_robot.py
@create at: 2017-10-24 10:57

这一行开始写关于本文件的说明与解释
"""

import json

from crwy.spider import BaseSpider
from crwy.exceptions import CrwyExtendException


class DingDingRobot(BaseSpider):
    def __init__(self, access_token=None,
                 api_url="https://oapi.dingtalk.com/robot/send?access_token="):
        super(DingDingRobot, self).__init__()
        if not api_url:
            raise CrwyExtendException('access_token unset.')
        self.api_url = api_url
        self.header = {'Content-Type': 'application/json'}
        self.access_token = access_token
        self.html_downloader.session.headers = self.header

    def send_text(self, content, at_mobiles=list(), is_at_all=False):
        try:
            data = {
                "text": {
                    "content": content
                },
                "msgtype": "text",
                "at": {
                    "isAtAll": is_at_all,
                    "atMobiles": at_mobiles
                }
            }

            res = self.html_downloader.download(
                self.api_url + self.access_token,
                method='POST',
                data=json.dumps(data))
            return res
        except Exception as e:
            raise CrwyExtendException(e)

    def send_markdown(self, title, content, at_mobiles=list(),
                      is_at_all=False):
        try:
            data = {
                "msgtype": "markdown",
                "markdown": {
                    "title": title,
                    "text": content
                },
                "at": {
                    "atMobiles": at_mobiles,
                    "isAtAll": is_at_all
                }
            }

            res = self.html_downloader.download(
                self.api_url + self.access_token,
                method='POST',
                data=json.dumps(data))
            return res
        except Exception as e:
            raise CrwyExtendException(e)

    def send_action_card(self, title, content, hide_avatar="0",
                         btn_oriengtation="0", single_title="阅读全文",
                         single_url="#"):
        try:
            data = {
                "actionCard": {
                    "title": title,
                    "text": content,
                    "hideAvatar": hide_avatar,
                    "btnOrientation": btn_oriengtation,
                    "singleTitle": single_title,
                    "singleURL": single_url
                },
                "msgtype": "actionCard"
            }
            res = self.html_downloader.download(
                self.api_url + self.access_token,
                method='POST',
                data=json.dumps(data))
            return res
        except Exception as e:
            raise CrwyExtendException(e)

    def send_feed_card(self, links):
        """

        :param links: array[{'title':'', 'messageURL':'', 'picURL':''}]
        :return:
        """
        try:
            data = {
                "feedCard": {
                    "links": links
                },
                "msgtype": "feedCard"
            }
            res = self.html_downloader.download(
                self.api_url + self.access_token,
                method='POST',
                data=json.dumps(data))
            return res
        except Exception as e:
            raise CrwyExtendException(e)

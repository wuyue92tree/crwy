#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: wuyue92tree@163.com

import inspect
from crwy.utils.html.html_downloader import HtmlDownloader
from crwy.utils.html.html_parser import HtmlParser
from crwy.utils.logger import Logger


class SpiderBase(object):
    """ Spider基础类 """
    def __init__(self):
        """
        初始化下载器/解析器及日志接口
        """
        self.html_downloader = HtmlDownloader()
        self.html_parser = HtmlParser()
        self.logger = Logger.rt_logger()
        self.worker = None
        self.proxies = None


class Spider(SpiderBase):
    """ Spider类 提供基本方法 """
    def __init__(self):
        super(Spider, self).__init__()

    def login(self, *args, **kwargs):
        pass

    def clean(self, *args, **kwargs):
        pass

    def save(self, *args, **kwargs):
        pass

    @staticmethod
    def func_name():
        """ 返回函数名称 """
        return inspect.stack()[1][3]

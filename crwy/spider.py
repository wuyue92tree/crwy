#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: wuyue92tree@163.com

import inspect
from crwy.utils.html.html_downloader import HtmlDownloader
from crwy.utils.html.html_parser import HtmlParser


class BaseSpider(object):
    """ Spider基础类 """
    def __init__(self):
        """
        初始化下载器/解析器及日志接口
        """
        self.html_downloader = HtmlDownloader()
        self.html_parser = HtmlParser()


class Spider(BaseSpider):
    """ Spider类 提供基本方法 """
    def __init__(self, logger=None):
        super(Spider, self).__init__()
        self.login_kwargs = None    # 用于存放登录时所需的参数
        self.proxies = None
        if logger:
            self.logger = logger
        else:
            from crwy.utils.logger import Logger
            self.logger = Logger.timed_rt_logger()

    def login(self, *args, **kwargs):
        pass

    def clean(self, *args, **kwargs):
        pass

    def save(self, *args, **kwargs):
        pass

    def get_cookie(self):
        pass

    @staticmethod
    def func_name():
        """ 返回函数名称 """
        return inspect.stack()[1][3]

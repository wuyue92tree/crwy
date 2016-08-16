#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: wuyue92tree@163.com

from crwy.utils.html.html_downloader import HtmlDownloader
from crwy.utils.html.html_parser import HtmlParser


class Spider(object):
    def __init__(self):
        self.html_downloader = HtmlDownloader()
        self.html_parser = HtmlParser()
#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: wuyue
@contact: wuyue92tree@163.com
@software: IntelliJ IDEA
@file: pyppeteer_api.py
@create at: 2019-03-24 17:04

这一行开始写关于本文件的说明与解释
"""

import asyncio
from crwy.spider import Spider

try:
    from pyppeteer import launch
except ImportError:
    pass


class PyppeteerApi(Spider):
    def __init__(self, logger=None, proxy=None, **kwargs):
        super(PyppeteerApi, self).__init__(logger=logger)


def main():
    executor = PyppeteerApi()
    # TODO


if __name__ == '__main__':
    main()

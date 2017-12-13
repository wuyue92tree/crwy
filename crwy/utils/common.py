#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: wuyue
@contact: wuyue92tree@163.com
@software: PyCharm
@file: common.py
@create at: 2017-12-12 18:01

这一行开始写关于本文件的说明与解释
"""


def cookie2str(cookies):
    """
    将requests 字典类型cookie转换成字符串
    :param cookies: dict
    :return: string
    """
    return '; '.join([name+'='+cookies.get(name) for name in cookies])


# if __name__ == '__main__':
#     main()

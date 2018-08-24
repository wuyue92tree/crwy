#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: wuyue
@contact: wuyue92tree@163.com
@software: PyCharm
@file: exceptions.py
@create at: 2017-12-13 14:14

这一行开始写关于本文件的说明与解释
"""


class CrwyException(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class CrwyImportException(CrwyException):
    pass


class CrwyKafkaException(CrwyException):
    pass


class CrwyMnsException(CrwyException):
    pass


class CrwyDbException(CrwyException):
    pass


class CrwyExtendException(CrwyException):
    pass


class CrwyCookieValidException(CrwyException):
    pass


class CrwyScrapyPlugsException(CrwyException):
    pass

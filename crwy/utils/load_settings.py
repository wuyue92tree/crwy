#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: wuyue
@contact: wuyue92tree@163.com
@software: PyCharm
@file: load_settings.py
@create at: 2018-06-20 19:32

这一行开始写关于本文件的说明与解释
"""

import consul
from crwy.exceptions import CrwyException


class LoadSettingsFromConsul(object):
    def __init__(self, **kwargs):
        self.c = consul.Consul(**kwargs)
        self.main_key = None

    def init_main_key(self, key=None):
        if not key:
            raise CrwyException('Please set key first.')
        self.main_key = key

    def _get_settings(self, key=None):
        self.init_main_key(key=key)
        index, data = self.c.kv.get(self.main_key, recurse=True)
        if not data:
            raise CrwyException('Please make sure the key: <%s> is exist.' %
                                self.main_key)

        new_data = {
            item.get('Key').split('/')[-1]: eval(item.get('Value'))
            for item in data
        }

        return new_data

    @classmethod
    def get_settings(cls, key=None, **kwargs):
        load_settings = cls(**kwargs)
        return load_settings._get_settings(key=key)

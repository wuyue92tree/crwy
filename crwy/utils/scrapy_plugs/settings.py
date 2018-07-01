#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: wuyue
@contact: wuyue92tree@163.com
@software: PyCharm
@file: settings.py
@create at: 2018-06-20 19:33

这一行开始写关于本文件的说明与解释
"""

from crwy.utils.load_settings import LoadSettingsFromConsul
from crwy.exceptions import CrwyException


class ScrapySettingsFromConsul(LoadSettingsFromConsul):
    def __init__(self, spider_name, bot_name, prefix='scrapy', **kwargs):
        super(ScrapySettingsFromConsul, self).__init__(**kwargs)
        self.spider_name = spider_name
        self.bot_name = bot_name
        self.prefix = prefix

    def init_main_key(self, key=None):
        if not key:
            self.main_key = '{prefix}/{bot_name}/{spider_name}'.format(
                prefix=self.prefix, bot_name=self.bot_name,
                spider_name=self.spider_name
            )
        else:
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
        new_data['SPIDER_NAME'] = self.spider_name

        return new_data

    @classmethod
    def get_settings(cls, spider_name, bot_name, key=None, prefix='scrapy',
                     **kwargs):
        load_settings = cls(spider_name, bot_name, prefix=prefix, **kwargs)
        return load_settings._get_settings(key=key)

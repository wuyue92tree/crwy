#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: wuyue
@contact: wuyue92tree@163.com
@software: PyCharm
@file: redis_m.py
@create at: 2017-12-26 14:50

这一行开始写关于本文件的说明与解释
"""

from crwy.exceptions import CrwyImportException
from crwy.decorates import cls2singleton

try:
    import redis
except ImportError:
    raise CrwyImportException(
        "You should install redis plugin first! try: pip install redis==2.10.6")


@cls2singleton
class RedisDb(object):
    def __init__(self, **kwargs):
        if 'url' in kwargs.keys():
            url = kwargs.pop('url')
            self.pool = redis.ConnectionPool.from_url(url, **kwargs)
        else:
            self.pool = redis.ConnectionPool(**kwargs)
        self.db = redis.StrictRedis(connection_pool=self.pool)


def get_redis_client(**kwargs):
    r = RedisDb(**kwargs)
    return r.db

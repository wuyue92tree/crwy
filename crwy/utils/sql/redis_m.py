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

try:
    import redis
except ImportError:
    raise CrwyImportException(
        "You should install redis plugin first! try: pip install redis")


def get_redis_client(**kwargs):
    pool = redis.ConnectionPool(**kwargs)
    return redis.StrictRedis(connection_pool=pool)

#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: wuyue92tree@163.com

from crwy.utils.sql import get_redis_client


class RedisHash(object):
    """Simple Hash with Redis Backend"""

    def __init__(self, name, **redis_kwargs):
        """
        The default connection parameters are:
        host='localhost', port=6379, db=0
        """
        self.__db = get_redis_client(**redis_kwargs)
        self.key = name

    def hget(self, item):
        """Return the approximate size of the queue."""
        return self.__db.hget(self.key, item)

    def hset(self, item, value):
        """Return True if the queue is empty, False otherwise."""
        return self.__db.hset(self.key, item, value)

    def hexists(self, item):
        return self.__db.hexists(self.key, item)

    def hlen(self):
        return self.__db.hlen(self.key)

    def clean(self):
        """Empty key"""
        return self.__db.delete(self.key)

    def db(self):
        return self.__db

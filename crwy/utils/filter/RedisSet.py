#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: wuyue92tree@163.com

from crwy.utils.sql import get_redis_client


class RedisSet(object):
    """Simple Deduplicate with Redis Backend"""

    def __init__(self, name, namespace='deduplicate', **redis_kwargs):
        """
        The default connection parameters are:
        host='localhost', port=6379, db=0
        """
        self.__db = get_redis_client(**redis_kwargs)
        self.key = '%s:%s' % (namespace, name)

    def sadd(self, item):
        """Return the approximate size of the queue."""
        if self.__db.sadd(self.key, item) == 0:
            return False
        else:
            return True

    def scard(self):
        """Return True if the queue is empty, False otherwise."""
        return self.__db.scard(self.key)

    def smembers(self):
        return self.__db.smembers(self.key)

    def clean(self):
        """Empty key"""
        return self.__db.delete(self.key)

    def db(self):
        return self.__db

#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: wuyue92tree@163.com

from crwy.utils.no_sql.redis_m import get_redis_client


class RedisHash(object):
    """Simple Hash with Redis Backend"""

    def __init__(self, name, server=None, **redis_kwargs):
        """
        The default connection parameters are:
        host='localhost', port=6379, db=0
        """
        if server:
            self.__db = server
        else:
            self.__db = get_redis_client(**redis_kwargs)
        self.key = name

    def hget(self, item):
        """Get item value."""
        return self.__db.hget(self.key, item)

    def hset(self, item, value):
        """Set item value."""
        return self.__db.hset(self.key, item, value)

    def hexists(self, item):
        """Is item exist."""
        return self.__db.hexists(self.key, item)

    def hlen(self):
        """Return total count."""
        return self.__db.hlen(self.key)

    def hkeys(self):
        return self.__db.hkeys(self.key)

    def clean(self):
        """Empty key"""
        return self.__db.delete(self.key)

    def db(self):
        return self.__db

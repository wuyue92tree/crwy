#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: wuyue92tree@163.com

from crwy.utils.no_sql.redis_m import get_redis_client


class RedisSet(object):
    """Simple Deduplicate with Redis Backend"""

    def __init__(self, name, namespace='deduplicate', server=None,
                 **redis_kwargs):
        """
        The default connection parameters are:
        host='localhost', port=6379, db=0
        """
        if server:
            self.__db = server
        else:
            self.__db = get_redis_client(**redis_kwargs)
        self.key = '%s:%s' % (namespace, name)

    def sadd(self, item):
        """Add item."""
        if self.__db.sadd(self.key, item) == 0:
            return False
        else:
            return True

    def srem(self, item):
        """Del item."""
        if self.__db.srem(self.key, item) == 0:
            return False
        else:
            return True

    def scard(self):
        """Return total count."""
        return self.__db.scard(self.key)

    def smembers(self):
        """Return all item."""
        return self.__db.smembers(self.key)

    def clean(self):
        """Empty key"""
        return self.__db.delete(self.key)

    def db(self):
        return self.__db

#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: wuyue92tree@163.com

from crwy.utils.no_sql.redis_m import get_redis_client


class RedisSortedSet(object):
    """Simple Sorted Deduplicate with Redis Backend"""

    def __init__(self, name, namespace='deduplicate_sorted', server=None,
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

    def zadd(self, score, item):
        """Add item."""
        if self.__db.zadd(self.key, score, item) == 0:
            return False
        else:
            return True

    def zrem(self, item):
        """Del item."""
        if self.__db.zrem(self.key, item) == 0:
            return False
        else:
            return True

    def zcard(self):
        """Return total count."""
        return self.__db.zcard(self.key)

    def zscore(self, item):
        """Return item score."""
        return self.__db.zscore(self.key, item)

    def zmembers(self):
        """Return all item."""
        return self.__db.zmembers(self.key)

    def clean(self):
        """Empty key"""
        return self.__db.delete(self.key)

    def db(self):
        return self.__db

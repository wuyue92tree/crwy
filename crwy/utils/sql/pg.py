#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: wuyue
@contact: wuyue92tree@163.com
@software: PyCharm
@file: pg.py
@create at: 2017-12-15 14:28

这一行开始写关于本文件的说明与解释
"""

from crwy.exceptions import CrwyImportException, CrwyDbException
from crwy.decorates import cls2singleton

try:
    import pgdb
except ImportError:
    raise CrwyImportException("You should install PyGreSQL first! try: pip "
                              "install PyGreSQL")
try:
    from DBUtils.PersistentPg import PersistentPg
except ImportError:
    raise CrwyImportException(
        "You should install DBUtils first! try: pip install "
        "dbutils")


@cls2singleton
class PgHandle(object):
    def __init__(self, **kwargs):
        self._pg_pool = PersistentPg(pgdb, **kwargs)

    def query_by_sql(self, sql):
        conn = self._pg_pool.connection()
        cur = conn.cursor()
        try:
            cur.execute(sql)
            result = cur.fetchall()
            return result
        except Exception as e:
            raise CrwyDbException(e)
        finally:
            cur.close()
            conn.close()

    def save(self, sql, data, many=False):
        conn = self._pg_pool.connection()
        cur = conn.cursor()
        try:
            if many is False:
                cur.execute(sql, data)
            else:
                cur.executemany(sql, data)
        except Exception as e:
            raise CrwyDbException(e)
        finally:
            cur.close()
            conn.close()

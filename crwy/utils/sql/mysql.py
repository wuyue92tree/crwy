#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: wuyue
@contact: wuyue92tree@163.com
@software: PyCharm
@file: mysql.py
@create at: 2017-12-15 14:20

这一行开始写关于本文件的说明与解释
"""

from crwy.exceptions import CrwyImportException, CrwyDbException

try:
    import MySQLdb
except ImportError:
    CrwyImportException("You should install MySQLdb first! try: pip install "
                        "mysql-python")
try:
    from DBUtils.PersistentDB import PersistentDB
except ImportError:
    CrwyImportException("You should install DBUtils first! try: pip install "
                        "dbutils")


class MysqlHandle(object):
    def __init__(self, **kwargs):
        self._mysql_pool = PersistentDB(MySQLdb, **kwargs)

    def query_by_sql(self, sql):
        conn = self._mysql_pool.connection()
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
        conn = self._mysql_pool.connection()
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

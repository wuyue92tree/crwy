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
from crwy.decorates import cls2singleton

try:
    import pymysql
except ImportError:
    raise CrwyImportException(
        "You should install pymysql first! try: pip install "
        "pymysql")
try:
    from DBUtils.PersistentDB import PersistentDB
except ImportError:
    raise CrwyImportException(
        "You should install DBUtils first! try: pip install "
        "dbutils")


@cls2singleton
class MysqlHandle(object):
    def __init__(self, **kwargs):
        self._mysql_pool = PersistentDB(pymysql, **kwargs)

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

    def save(self, sql, data, many=False, get_last_insert_id=False):
        conn = self._mysql_pool.connection()
        cur = conn.cursor()
        try:
            if many is False:
                cur.execute(sql, data)
            else:
                cur.executemany(sql, data)
            conn.commit()

            if get_last_insert_id is False:
                return

            cur.execute("select last_insert_id() as id")
            res = cur.fetchone()
            if isinstance(res, tuple):
                return res[0]
            elif isinstance(res, dict):
                return res.get('id')
            else:
                return res

        except Exception as e:
            raise CrwyDbException(e)
        finally:
            cur.close()
            conn.close()

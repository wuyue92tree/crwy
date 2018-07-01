#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: wuyue
@contact: wuyue92tree@163.com
@software: PyCharm
@file: pipelines.py
@create at: 2018-06-15 15:26

这一行开始写关于本文件的说明与解释
"""

import logging
from pymysql.cursors import DictCursor
from crwy.utils.sql.mysql import MysqlHandle


class MysqlSavePipeline(object):
    def __init__(self, db_name=None, db_host=None, db_port=None,
                 db_username=None, db_password=None, db_charset=None,
                 db_cursorclass=None):
        self.db_name = db_name
        self.db_host = db_host
        self.db_port = db_port
        self.db_username = db_username
        self.db_password = db_password
        self.db_charset = db_charset
        self.db_cursorclass = db_cursorclass
        self.logger = logging.getLogger(__name__)
        self.mysql_handle = None

    @classmethod
    def from_crawler(cls, crawler):
        """
        loading mysql settings
        :param crawler: 
        :return: 
        """
        settings = crawler.settings
        db_name = settings.get('MYSQL_DB_NAME', '')
        db_host = settings.get('MYSQL_DB_HOST', '127.0.0.1')
        db_port = settings.getint('MYSQL_DB_PORT', 3306)
        db_username = settings.get('MYSQL_DB_USERNAME', 'root')
        db_password = settings.get('MYSQL_DB_PASSWORD', '123456')
        db_charset = settings.get('MYSQL_DB_CHARSET', 'utf8')
        db_cursorclass = settings.get('MYSQL_DB_CURSORCLASS', DictCursor)
        return cls(db_name=db_name, db_host=db_host, db_port=db_port,
                   db_username=db_username,
                   db_password=db_password,
                   db_charset=db_charset,
                   db_cursorclass=db_cursorclass)

    def process_item(self, item, spider):
        self.insert_db(item)
        return item

    def open_spider(self, spider):
        """
        init mysql_handle object
        :param spider: 
        :return: 
        """
        self.mysql_handle = MysqlHandle(
            host=self.db_host,
            port=self.db_port,
            user=self.db_username,
            password=self.db_password,
            db=self.db_name,
            charset=self.db_charset,
            cursorclass=self.db_cursorclass
        )

    def insert_db(self, item):
        """        
        -----------------------------------
        Do something here with mysql_handle
        -----------------------------------
        
        eg:
        sql = None
        data = None
        last_insert_id = self.mysql_handle.save(
            sql, data, get_last_insert_id=True)
        self.logger.info('item saved succcess to mysql: %s' % last_insert_id)
        """
        pass


#!/usr/local/bin/python
# -*- coding: utf-8 -*-
# author: wuyue92tree@163.com

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from crwy.decorates import cls2singleton

Base = declarative_base()


@cls2singleton
class SqlalchemyHandle(object):
    """
    以ORM的方式连接数据库
    """

    def __init__(self, db_url, **kwargs):
        self.engine = create_engine(db_url, **kwargs)
        DBSession = sessionmaker(bind=self.engine)
        self.session = DBSession()

    def init_table(self):
        return Base.metadata.create_all(self.engine)

    def delete_table(self):
        return Base.metadata.drop_all(self.engine)

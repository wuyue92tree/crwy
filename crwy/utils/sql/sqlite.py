#!/usr/local/bin/python
# -*- coding: utf-8 -*-
# author: wuyue92tree@163.com

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Sqlite(object):
    def __init__(self, database):
        self.engine = create_engine('sqlite:///data/%s.db' % database)
        DBSession = sessionmaker(bind=self.engine)
        self.session = DBSession()

    def init_table(self):
        return Base.metadata.create_all(self.engine)

    def delete_table(self):
        return Base.metadata.drop_all(self.engine)

#!/usr/local/bin/python
# -*- coding: utf-8 -*-
# author: wuyue92tree@163.com

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Mysql(object):
    def __init__(self,
                 username,
                 password,
                 database,
                 host='127.0.0.1',
                 port='3306',
                 charset='utf8'):
        self.engine = create_engine(
            'mysql+mysqldb://%s:%s@%s:%s/%s?charset=%s' %
            (username, password, host, port, database, charset))
        DBSession = sessionmaker(bind=self.engine)
        self.session = DBSession()

    def init_table(self):
        return Base.metadata.create_all(self.engine)

    def delete_table(self):
        return Base.metadata.drop_all(self.engine)

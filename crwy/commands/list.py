#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: wuyue92tree@163.com

from __future__ import print_function
import os
import sys


class Command(object):
    @staticmethod
    def get_spider_list():
        spider_list = []
        for a, b, c in os.walk('src'):
            for i in c:
                if i == '__init__.py':
                    continue
                if '.pyc' in i:
                    continue
                if '_db' in i:
                    continue
                if '.py' in i:
                    i = i.split('.')[0]
                    spider_list.append(i)
        return spider_list

    def main(self):
        spider_list = self.get_spider_list()

        if len(spider_list) == 0:
            print('No spider found!!!')
            sys.exit(1)

        for spider in spider_list:
            print(spider)

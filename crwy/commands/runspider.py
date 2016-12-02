#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: wuyue92tree@163.com

from __future__ import print_function
import sys
# import os

from optparse import OptionParser
from crwy.commands.list import Command as ListCommand


class Command(object):
    def execute(self, spider_name):
        module = __import__('src.%s' % spider_name)
        cls_obj = getattr(
            getattr(module, spider_name), spider_name.capitalize() + 'Spider')
        spider = cls_obj()
        res = spider.run()
        return res

    def main(self):
        Usage = "Usage:  crwy runspider [option] [args]"
        parser = OptionParser(Usage)
        parser.add_option(
            '-n', '--name', dest='name', help='spider name', metavar="NAME")
        opt, args = parser.parse_args()

        if len(args) < 1:
            print(Usage)
            sys.exit(1)

        if opt.name is not None:
            if opt.name in ListCommand.get_spider_list():
                sys.path.append('.')
                self.execute(opt.name)
            else:
                print('ERROR spider: "%s" is not found!!!' % opt.name)
                sys.exit(1)

#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: wuyue92tree@163.com

from __future__ import print_function
import sys
from optparse import OptionParser
from multiprocessing import Process
from crwy.commands.list import Command as ListCommand


class Command(object):
    def execute(self, spider_name):
        module = __import__('src.%s' % spider_name)
        cls_obj = getattr(
            getattr(module, spider_name), spider_name.capitalize() + 'Spider')
        spider = cls_obj()
        res = spider.run()
        return res

    def multi_execute(self, spider_name, process):
        try:
            process = int(process)
        except ValueError:
            print('ERROR: process must be int!!!')
            sys.exit(1)
        process_list = []
        for i in range(process):
            p = Process(target=self.execute,
                        args=(spider_name,),
                        name='%s_%s' % (spider_name, i))
            p.start()
            process_list.append(p)

        for p in process_list:
            p.join()

    def main(self):
        Usage = "Usage:  crwy runspider [option] [args]"
        parser = OptionParser(Usage)
        parser.add_option(
            '-n', '--name', dest='name', help='spider name', metavar="NAME")
        parser.add_option(
            '-p', '--process', dest='process', help='crawler by multi process', metavar="PROCESS")
        opt, args = parser.parse_args()

        if len(args) < 1:
            print(Usage)
            sys.exit(1)

        if opt.name is not None:
            if opt.name in ListCommand.get_spider_list():
                sys.path.append('.')

                if opt.process is not None:
                    self.multi_execute(opt.name, opt.process)
                else:
                    self.execute(opt.name)
            else:
                print('ERROR spider: "%s" is not found!!!' % opt.name)
                sys.exit(1)

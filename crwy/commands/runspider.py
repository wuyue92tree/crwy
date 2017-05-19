#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: wuyue92tree@163.com

from __future__ import print_function
import sys
import gevent
from optparse import OptionParser
from crwy.commands.list import Command as ListCommand


class Command(object):
    def execute(self, spider_name, worker):
        module = __import__('src.%s' % spider_name)
        cls_obj = getattr(
            getattr(module, spider_name), spider_name.capitalize() + 'Spider')

        spider = cls_obj()
        spider.worker = worker
        res = spider.run()
        return res

    def multi_execute(self, spider_name, coroutine):
        try:
            coroutine = int(coroutine)
        except ValueError:
            print('ERROR: process must be int!!!')
            sys.exit(1)

        from gevent import monkey
        monkey.patch_all()

        gevent.joinall([
            gevent.spawn(self.execute, spider_name, 'worker%d' % i) for i in
            range(coroutine)
        ])

    def main(self):
        Usage = "Usage:  crwy runspider [option] [args]"
        parser = OptionParser(Usage)
        parser.add_option(
            '-n', '--name', dest='name', help='spider name', metavar="NAME")
        parser.add_option(
            '-c', '--coroutine', dest='coroutine',
            help='crawler by multi coroutine', metavar="COROUTINE")
        opt, args = parser.parse_args()

        if len(args) < 1:
            print(Usage)
            sys.exit(1)

        if opt.name is not None:
            if opt.name in ListCommand.get_spider_list():
                sys.path.append('.')

                if opt.coroutine is not None:
                    self.multi_execute(opt.name, opt.coroutine)
                else:
                    self.execute(opt.name, 'worker0')
            else:
                print('ERROR spider: "%s" is not found!!!' % opt.name)
                sys.exit(1)

#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: wuyue92tree@163.com

from __future__ import print_function
import sys
import gevent
import threading
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

    def multi_coroutine(self, spider_name, coroutine):
        try:
            coroutine = int(coroutine)
        except ValueError:
            print('ERROR: coroutine must be int!!!')
            sys.exit(1)

        from gevent import monkey
        monkey.patch_all()

        gevent.joinall([
            gevent.spawn(self.execute, spider_name) for i in
            xrange(coroutine)
        ])

    def multi_thread(self, spider_name, thread):
        try:
            thread = int(thread)
        except ValueError:
            print('ERROR: thread must be int!!!')
            sys.exit(1)

        thread_list = []
        for i in xrange(thread):
            t = threading.Thread(target=self.execute, args=(spider_name,))
            t.start()
            thread_list.append(t)

        for t in thread_list:
            t.join()

    def main(self):
        Usage = "Usage:  crwy runspider [option] [args]"
        parser = OptionParser(Usage)
        parser.add_option(
            '-n', '--name', dest='name', help='spider name', metavar="NAME")
        parser.add_option(
            '-c', '--coroutine', dest='coroutine',
            help='crawler by multi coroutine', metavar="COROUTINE")
        parser.add_option(
            '-t', '--thread', dest='thread',
            help='crawler by multi thread', metavar="THREAD")
        opt, args = parser.parse_args()

        if opt.name is not None:
            if opt.name in ListCommand.get_spider_list():
                sys.path.append('.')

                if opt.coroutine and opt.thread:
                    print("Can not run use both coroutine and thread!")
                    sys.exit(1)

                if opt.coroutine is not None:
                    self.multi_coroutine(opt.name, opt.coroutine)
                elif opt.thread is not None:
                    self.multi_thread(opt.name, opt.thread)
                else:
                    self.execute(opt.name)
            else:
                print('ERROR spider: "%s" is not found!!!' % opt.name)
                sys.exit(1)
        else:
            print(Usage)
            sys.exit(1)

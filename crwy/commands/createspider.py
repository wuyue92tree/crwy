#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: wuyue92tree@163.com

from __future__ import print_function

import sys
import os
from optparse import OptionParser
from crwy.settings.default_settings import TEMPLATE_DIR
from crwy.changetmpl import change_spider_name
from crwy.commands.list import Command as ListCommand

PATH = os.path.join(TEMPLATE_DIR, 'spider')
TMPLATE_PATH = os.path.join(PATH, '%s.py.tmpl')
SPIDER_TMPL_LIST = ['basic', 'sqlite', 'queue', 'redis_queue']


class Command(object):
    def create_spider(self, name, tmpl):
        spider_list = ListCommand.get_spider_list()
        if name in spider_list:
            print('[ERROR] spider "%s" is exists!!!' % name)
            sys.exit(1)

        path = TMPLATE_PATH % tmpl
        spider = change_spider_name(name, path)
        f = open('src/%s.py' % name, 'w')
        f.write(spider)
        print('Spider is base on : %s template' % tmpl)
        print('Create spider : "%s" success!!!' % name)

    def main(self):
        Usage = "Usage:  crwy createspider [option] [args]"
        parser = OptionParser(Usage)
        parser.add_option('-t', '--tmpl', dest='template', help='spider template', metavar="TEMPLATE")
        parser.add_option('-n', '--name', dest='name', help='new spider name', metavar="NAME")
        opt, args = parser.parse_args()

        if len(args) < 1:
            print(Usage)
            sys.exit(1)

        if opt.template is None:
            tmpl = 'basic'

        if opt.template is not None:
            if opt.template in SPIDER_TMPL_LIST:
                tmpl = opt.template
                global tmpl
            else:
                print('[ERROR] Illegal template name!!!')
                sys.exit(1)

        if opt.name is not None:
            name = opt.name
        else:
            print('[ERROR] Please enter a spider name!!!')
            sys.exit(1)

        self.create_spider(name, tmpl)

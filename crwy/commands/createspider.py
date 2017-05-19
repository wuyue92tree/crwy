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
        parser.add_option(
            '-l',
            '--list',
            action='store_true',
            dest='list',
            help='list available spider template name',
            metavar="LIST")
        parser.add_option(
            '-p',
            '--preview',
            dest='preview',
            help='preview spider template',
            metavar="PREVIEW")
        parser.add_option(
            '-t',
            '--tmpl',
            dest='template',
            help='spider template',
            metavar="TEMPLATE")
        parser.add_option(
            '-n',
            '--name',
            dest='name',
            help='new spider name',
            metavar="NAME")

        opt, args = parser.parse_args()
        # print(opt)
        if not opt.name and not opt.list and not opt.template and not opt.preview:
            print(Usage)
            sys.exit(1)

        if opt.list:
            print('Available template:')
            for template in SPIDER_TMPL_LIST:
                print('  %s' % template)
            sys.exit(1)

        if opt.preview is not None:
            if opt.preview in SPIDER_TMPL_LIST:
                print(open(TMPLATE_PATH % opt.preview, 'r').read())
                sys.exit(1)
            else:
                print('[ERROR] Illegal template name!!!')
                sys.exit(1)

        if opt.template is not None:
            if opt.template in SPIDER_TMPL_LIST:
                tmpl = opt.template
            else:
                print('[ERROR] Illegal template name!!!')
                sys.exit(1)
        else:
            tmpl = 'basic'

        if opt.name is not None:
            name = opt.name
        else:
            print('[ERROR] Please enter a spider name!!!')
            sys.exit(1)

        self.create_spider(name, tmpl)

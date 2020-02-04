#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: wuyue92tree@163.com

from __future__ import print_function
import os
import shutil
import scrapy
from optparse import OptionParser
from crwy import version
from crwy.settings.default_settings import TEMPLATE_DIR

CRWY_SPIDER_TEMPLATE_DIR = os.path.join(TEMPLATE_DIR, 'spiders')
SCRAPY_SPIDER_TEMPLATE_DIR = os.path.join(scrapy.__path__[0],
                                          'templates/spiders')


def install():
    scrapy_tmpl = os.listdir(SCRAPY_SPIDER_TEMPLATE_DIR)
    for tmpl in os.listdir(CRWY_SPIDER_TEMPLATE_DIR):
        if tmpl in scrapy_tmpl:
            print('{} exist.'.format(tmpl))
            continue
        shutil.copy(os.path.join(CRWY_SPIDER_TEMPLATE_DIR, tmpl),
                    os.path.join(SCRAPY_SPIDER_TEMPLATE_DIR, tmpl))
        print('{} installed.'.format(tmpl))


def uninstall():
    crwy_tmpl = os.listdir(CRWY_SPIDER_TEMPLATE_DIR)
    for tmpl in os.listdir(SCRAPY_SPIDER_TEMPLATE_DIR):
        if tmpl not in crwy_tmpl:
            print('{} not match, skip.'.format(tmpl))
            continue
        os.remove(os.path.join(SCRAPY_SPIDER_TEMPLATE_DIR, tmpl))
        print('{} uninstalled.'.format(tmpl))
    pass


def execute():
    parser = OptionParser(usage="Usage: crwy [options] arg1 arg2")
    parser.add_option('-i', '--install', action="store_true",
                      help='install crwy tmpl for scrapy')
    parser.add_option('-u', '--uninstall', action="store_true",
                      help='uninstall crwy tmpl for scrapy')
    parser.add_option('-v', '--version', action="store_true",
                      help='print version')
    options, args = parser.parse_args()
    if options.version:
        print(version)
    elif options.install:
        install()
    elif options.uninstall:
        uninstall()
    else:
        parser.print_help()


if __name__ == '__main__':
    execute()

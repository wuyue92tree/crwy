#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: wuyue92tree@163.com

from __future__ import print_function
import sys
import os

from configparser import ConfigParser
from optparse import OptionParser
from crwy.commands.list import Command as ListCommand


class Command(object):
    def get_project_settings(self):
        conf = ConfigParser()
        conf.read('crwy.cfg', encoding='utf-8')
        settings = conf.get('settings', 'default').encode('utf-8')
        return settings

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
            console = os.popen('python src/%s.py' % opt.name).read()
            print(console)

#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: wuyue92tree@163.com

import sys
import os
from optparse import OptionParser


class Command(object):
    def main(self):
        Usage = "Usage:  crwy createspider [option] [args]"
        parser = OptionParser(Usage)
        parser.add_option('-t', '--tmpl', dest='template', help='spider template', metavar="TEMPLATE")
        parser.add_option('-n', '--name', dest='name', help='new spider name', metavar="NAME")
        opt, args = parser.parse_args()

        if len(args) < 2:
            print Usage
            sys.exit(1)

        if opt.template is not None:
            pass

        if opt.name is not None:
            pass
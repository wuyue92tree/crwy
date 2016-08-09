#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: wuyue92tree@163.com

import sys

from optparse import OptionParser


class Command(object):
    def main(self):
        Usage = "Usage:  crwy runspider [option] [args]"
        parser = OptionParser(Usage)
        parser.add_option('-p', '--path', dest='args', help='path to spider', metavar="PATH")
        opt, args = parser.parse_args()

        # print args
        if len(args) < 2:
            print Usage
            sys.exit(1)

    def run(self):
        self.main()
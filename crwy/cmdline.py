#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: wuyue92tree@163.com

import sys

from commands.crawl import Command as CrawlCommand


def execute():
    Usage = 'Usage:\n  crwy commands [option] [args]\n'
    project_list = ['crawl', 'aaa', 'bbb', 'ccc']
    Options = 'Avaliable Commands:\n  %s\n' % 'crawl'
    Notice = 'Use "crwy <command> -h" to see more info about a command'
    # print sys.argv
    if len(sys.argv) < 2:
        print Usage
        print Options
        print Notice
        sys.exit(1)

    project = sys.argv[1]

    if project not in project_list:
        print Usage
        print Options
        print Notice
        sys.exit()

    if project == 'crawl':
        cmd = CrawlCommand()
        cmd.run()


if __name__ == '__main__':
    execute()
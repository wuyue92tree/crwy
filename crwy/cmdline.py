#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: wuyue92tree@163.com

import sys
import os

from commands.runspider import Command as RunspiderCommand
from commands.startproject import Command as StartprojectCommand


def under_conf():
    if os.path.exists('config.py'):
        return True
    else:
        return False


def execute():
    if under_conf():
        import config

        Header = 'Crwy 1.0.0 - active\n'
    else:
        Header = 'Crwy 1.0.0 - no active project found!!!\n'

    Usage = 'Usage:\n  crwy <commands> [option] [args]\n'
    project_list = ['runspider', 'startproject', 'createspider']
    Options = 'Avaliable Commands:\n  runspider\trun a spider\n  startproject\tcreate a new project\n  createspider\tcreate a new spider\n'
    Notice = 'Use "crwy <command> -h" to see more info about a command'
    # print sys.argv
    if len(sys.argv) < 2:
        print Header
        print Usage
        print Options
        print Notice
        sys.exit(1)

    project = sys.argv[1]

    if project not in project_list:
        print Header
        print Usage
        print Options
        print Notice
        sys.exit()

    if project == 'runspider':
        if under_conf():
            cmd = RunspiderCommand()
            cmd.main()
        else:
            print '[ERROR] No active project found!!!'
    if project == 'startproject':
        cmd = StartprojectCommand()
        cmd.main()


if __name__ == '__main__':
    execute()
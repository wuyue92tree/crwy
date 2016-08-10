#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: wuyue92tree@163.com

import sys
import os

from configparser import ConfigParser
from crwy.commands.runspider import Command as RunspiderCommand
from crwy.commands.startproject import Command as StartprojectCommand
from crwy.commands.createspider import Command as CreatespiderCommand


def under_conf():
    if os.path.exists('crwy.cfg'):
        return True
    else:
        return False


def get_project_name():
    conf = ConfigParser()
    conf.read('crwy.cfg', encoding='utf-8')
    project_name = conf.get('project', 'project_name').encode('utf-8')
    return project_name


def execute():
    if under_conf():
        Header = 'Crwy 1.0.0 - project: %s \n' % get_project_name()
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
        sys.exit(1)

    if project == 'startproject':
        cmd = StartprojectCommand()
        cmd.main()

    if project == 'runspider':
        if under_conf():
            cmd = RunspiderCommand()
            cmd.main()
        else:
            print '[ERROR] Please makesure that you are under project path!!!'

    if project == 'createspider':
        if under_conf():
            cmd = CreatespiderCommand()
            cmd.main()
        else:
            print '[ERROR] Please makesure that you are under project path!!!'

if __name__ == '__main__':
    execute()
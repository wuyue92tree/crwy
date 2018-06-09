#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: wuyue92tree@163.com

from __future__ import print_function
import sys
import os

from crwy.commands.runspider import Command as RunspiderCommand
from crwy.commands.startproject import Command as StartprojectCommand
from crwy.commands.createspider import Command as CreatespiderCommand
from crwy.commands.list import Command as ListCommand
from crwy.settings.default_settings import BASE_DIR

try:
    import ConfigParser
except ImportError:
    from configparser import ConfigParser


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


def get_project_settings():
    conf = ConfigParser()
    conf.read('crwy.cfg', encoding='utf-8')
    settings = conf.get('settings', 'default').encode('utf-8')
    return settings


def execute():
    if under_conf():
        Header = 'Crwy - project: %s \n' % get_project_name()
    else:
        Header = 'Crwy - no active project found!!!\n'

    Usage = 'Usage:\n  crwy <commands> [option] [args]\n'
    project_list = ['runspider', 'startproject', 'createspider', 'list',
                    'version']
    Options = 'Avaliable Commands:\n' \
              '  list\t\tlist all spider in your project\n' \
              '  runspider\trun a spider\n' \
              '  startproject\tcreate a new project\n' \
              '  createspider\tcreate a new spider\n' \
              '  version\tshow version\n'

    Notice = 'Use "crwy <command> -h" to see more info about a command'
    # print sys.argv
    if len(sys.argv) < 2:
        print(Header)
        print(Usage)
        print(Options)
        print(Notice)
        sys.exit(1)

    project = sys.argv[1]

    if project not in project_list:
        print(Header)
        print(Usage)
        print(Options)
        print(Notice)
        sys.exit(1)

    if project == 'startproject':
        cmd = StartprojectCommand()
        cmd.main()

    if project == 'runspider':
        if under_conf():
            cmd = RunspiderCommand()
            cmd.main()
        else:
            print('[ERROR] Please makesure that you are under project path!!!')

    if project == 'createspider':
        if under_conf():
            cmd = CreatespiderCommand()
            cmd.main()
        else:
            print('[ERROR] Please makesure that you are under project path!!!')

    if project == 'list':
        if under_conf():
            cmd = ListCommand()
            cmd.main()
        else:
            print('[ERROR] Please makesure that you are under project path!!!')

    if project == 'version':
        version_path = os.path.join(BASE_DIR, 'VERSION')
        print(open(version_path, 'r').read())


if __name__ == '__main__':
    execute()

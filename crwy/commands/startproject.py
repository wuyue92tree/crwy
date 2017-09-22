#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: wuyue92tree@163.com

from __future__ import print_function
import sys
import os
import shutil

from crwy.settings.default_settings import TEMPLATE_DIR
from crwy.changetmpl import change_project_name

PATH = os.path.join(TEMPLATE_DIR, 'project')
DATA_PATH = os.path.join(PATH, 'data')
SRC_PATH = os.path.join(PATH, 'src')
LOG_PATH = os.path.join(PATH, 'log')
CONFIG_PATH = os.path.join(PATH, 'crwy.cfg.tmpl')
SETTINGS_PATH = os.path.join(PATH, 'settings.py.tmpl')
LOGCONFIG_PATH = os.path.join(PATH, 'logger.conf.tmpl')


class Command(object):
    def create_project(self, project_name):
        os.mkdir(project_name)
        os.mkdir(project_name + '/conf')
        shutil.copytree(DATA_PATH, project_name + '/' + 'data')
        shutil.copytree(SRC_PATH, project_name + '/' + 'src')
        shutil.copytree(LOG_PATH, project_name + '/' + 'log')
        shutil.copy(LOGCONFIG_PATH, project_name + '/conf/logger.conf')

        config = change_project_name(project_name, CONFIG_PATH)
        f1 = open(project_name + '/crwy.cfg', 'w')
        f1.write(config)

        settings = change_project_name(project_name, SETTINGS_PATH)
        f2 = open(project_name + '/conf/settings.py', 'w')
        f2.write(settings)

        f3 = open(project_name + '/conf/__init__.py', 'w')
        f3.write('')

    def main(self):
        Usage = "Usage:  crwy startproject <project_name>\n"

        try:
            project_name = sys.argv[2]
            if project_name == '-h':
                print(Usage)
                print("  Add a new project")
                sys.exit(1)

            if os.path.exists(project_name):
                print('[ERROR] Path "%s" has exists!!!' % project_name)
            else:

                self.create_project(project_name)

                print("Project start......enjoy^.^")
        except IndexError:
            print(Usage)
            print("[ERROR] Please enter a project_name!!!")

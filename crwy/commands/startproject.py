#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: wuyue92tree@163.com


import sys
import os
import shutil

from crwy.settings.default_settings import BASE_DIR


class Command(object):
    def main(self):
        Usage = "Usage:  crwy startproject <project_name>\n"
        # print sys.argv
        try:
            project_name = sys.argv[2]
            if project_name == '-h':
                print Usage
                print "  Add a new project"
                sys.exit(1)
            # print project_name
            if os.path.exists(project_name):
                print '[ERROR] Path "%s" has exists!!!' % project_name
            else:
                os.mkdir(project_name)
                os.mkdir(project_name + '/' + project_name)
                shutil.copy(BASE_DIR+'/config.py', project_name)
                print "Project start......enjoy^.^"
        except IndexError:
            print Usage
            print "[ERROR] Please enter a project_name!!!"

        # os.mkdir()

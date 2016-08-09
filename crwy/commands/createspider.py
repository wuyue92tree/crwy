#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: wuyue92tree@163.com

import sys
import os


class Command(object):
    def main(self):
        project_name = sys.argv[3]
        print project_name
        # os.mkdir()

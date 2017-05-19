#! /usr/bin/env python
# -*- coding: utf-8 -*-
# Author: wuyue
# Email: wuyue@mofanghr.com


import logging
import logging.config
from crwy.cmdline import get_project_name

logging.config.fileConfig('./%s/default_logger.conf' % get_project_name())


class Logger(object):
    @staticmethod
    def file_logger():
        return logging.getLogger('fileLogger')

    @staticmethod
    def rt_logger():
        return logging.getLogger('rtLogger')

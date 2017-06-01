#! /usr/bin/env python
# -*- coding: utf-8 -*-
# Author: wuyue
# Email: wuyue@mofanghr.com


import logging
import logging.config
from configparser import NoSectionError

try:
    from crwy.cmdline import get_project_name
except ImportError:
    pass

try:
    logging.config.fileConfig('./%s/default_logger.conf' % get_project_name())
except NoSectionError:
    pass


class Logger(object):
    @staticmethod
    def file_logger():
        return logging.getLogger('fileLogger')

    @staticmethod
    def rt_logger():
        return logging.getLogger('rtLogger')

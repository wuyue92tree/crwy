#! /usr/bin/env python
# -*- coding: utf-8 -*-
# Author: wuyue
# Email: wuyue@mofanghr.com


import logging
import logging.config

try:
    logging.config.fileConfig('./conf/logger.conf')
except:
    pass


class Logger(object):
    @staticmethod
    def file_logger():
        return logging.getLogger('fileLogger')

    @staticmethod
    def rt_logger():
        return logging.getLogger('rtLogger')

    @staticmethod
    def timed_rt_logger():
        return logging.getLogger('timedRtLogger')

    @staticmethod
    def extra_logger(name=None):
        return logging.getLogger(name)

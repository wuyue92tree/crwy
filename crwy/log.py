#!/usr/bin/env python
# coding=utf-8

import logging
import time


class Log(object):
    def setup(self,
              level=logging.DEBUG,
              console=False,
              path='./log/',
              name='log'):
        filename = path + '%s_%s.log' % (name, time.strftime(
            '%Y-%m-%d', time.localtime(time.time())))
        self.logger = logging.getLogger(name)
        self.logger.setLevel(level)
        fmt = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        flog = logging.FileHandler(filename)
        flog.setFormatter(fmt)
        flog.setLevel(level)
        self.logger.addHandler(flog)

        if console:
            console = logging.StreamHandler()
            console.setLevel(logging.INFO)
            fmt = logging.Formatter('%(name)-12s- %(levelname)-8s %(message)s')
            console.setFormatter(fmt)
            self.logger.addHandler(console)

    def debug(self, message):
        self.logger.debug(message)

    def info(self, message):
        self.logger.info(message)

    def error(self, message):
        self.logger.error(message)

    def warning(self, message):
        self.logger.warning(message)

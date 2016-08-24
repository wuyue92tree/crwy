#!/usr/bin/env python
# coding=utf-8

import logging
import time


class Log(object):
    def setup(self,
              level=logging.DEBUG,
              console=False,
              path='./log/',
              name='log',
              mode='a'):
        logging.basicConfig(
            level=level,
            format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
            datefmt='%a, %d %b %Y %H:%M:%S',
            filename=path + '%s_%s.log' %
            (name, time.strftime('%Y-%m-%d', time.localtime(time.time()))),
            filemode=mode)
        if console:
            console = logging.StreamHandler()
            console.setLevel(logging.INFO)
            formatter = logging.Formatter(
                '%(name)-12s: %(levelname)-8s %(message)s')
            console.setFormatter(formatter)
            logging.getLogger('').addHandler(console)

    def debug(self, message):
        logging.debug(message)

    def info(self, message):
        logging.info(message)

    def warning(self, message):
        logging.warning(message)

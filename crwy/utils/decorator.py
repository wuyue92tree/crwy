#! /usr/bin/env python
# -*- coding: utf-8 -*-
# Author: wuyue
# Email: wuyue@mofanghr.com

from __future__ import print_function


def retry(attempt):
    """ 异常重试 """
    def decorator(func):
        def wrapper(*args, **kwargs):
            att = 0
            while att < attempt:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    att += 1
                    print("Got a error: %s !retry -------------------> %d" %
                          (repr(e), att))
        return wrapper
    return decorator


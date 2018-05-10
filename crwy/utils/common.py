#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: wuyue
@contact: wuyue92tree@163.com
@software: PyCharm
@file: common.py
@create at: 2017-12-12 18:01

这一行开始写关于本文件的说明与解释
"""

import os
import datetime
import ConfigParser
import re

__all__ = ['cookie2str', 'cookie2dict', 'config_handle', 'file_handle']


def cookie2str(cookie_dict):
    """
    将requests 字典类型cookie转换成字符串
    :param cookie_dict: dict
    :return: string
    """
    return '; '.join(
        [name + '=' + cookie_dict.get(name) for name in cookie_dict])


def cookie2dict(cookie_str):
    """
    将cookie_str转换成requests可用的dict类型
    :param cookie_str: string
    :return: dict
    """
    cookie_dict = dict()
    for item in cookie_str.strip().split(';'):
        name, value = item.split('=')
        cookie_dict[name] = value
    return cookie_dict


def datetime2str(target, fmt='%Y-%m-%d %H:%M:%S'):
    """
    将datetime对象转换成字符串
    :param target: datetime
    :param fmt: string
    :return: string
    """
    return datetime.datetime.strftime(target, fmt)


def str2datetime(target, fmt='%Y-%m-%d %H:%M:%S'):
    """
    将string转换成datetime对象
    :param target: string
    :param fmt: string
    :return: datetime
    """
    return datetime.datetime.strptime(target, fmt)


def dict2obj(target):
    """
    将dict转换成obj对象
    :param target: dict
    :return: obj
    """

    class Obj(object):
        def __init__(self, d):
            for a, b in d.items():
                if isinstance(b, (list, tuple)):
                    setattr(self, a,
                            [Obj(x) if isinstance(x, dict) else x for x in b])
                else:
                    setattr(self, a, Obj(b) if isinstance(b, dict) else b)

    return Obj(target)


def obj2dict(target):
    """
    将obj对象转换成dict
    :param target: obj
    :return: dict
    """
    return target.__dict__


def config_handle(path):
    """
    用于对Config配置文件进行操作，初始化config_path
    :param path: config文件路径
    :return: 返回config对象
    """
    config = ConfigParser.ConfigParser()
    config.read(path)
    return config


def file_handle(path, file_name, mode='r'):
    """
    用于对普通文件进行操作
    :param path: 文件路径
    :param file_name: 文件名称
    :param mode: 加载模式，默认'r'
    :return: file对象
    """
    if path[-1] == '/':
        real_path = path + file_name
    else:
        real_path = path + '/' + file_name

    if not os.path.exists(path):
        os.makedirs(path)

    return open(real_path, mode=mode)


def remove_emoji(content):
    """
    表情符去除
    :param content: unicode
    :return: unicode
    """
    pattern = re.compile(
        u"(\ud83d[\ude00-\ude4f])|"  # emoticons
        u"(\ud83c[\udf00-\uffff])|"  # symbols & pictographs (1 of 2)
        u"(\ud83d[\u0000-\uddff])|"  # symbols & pictographs (2 of 2)
        u"(\ud83d[\ude80-\udeff])|"  # transport & map symbols
        u"(\ud83c[\udde0-\uddff])"  # flags (iOS)
        "+", flags=re.UNICODE)
    return pattern.sub(r'', content)


def change_kv(dict_ori):
    """
    字典kv调换
    :param dict_ori: 原字典
    :return: 新字典
    """
    return dict(zip(dict_ori.values(), dict_ori.keys()))


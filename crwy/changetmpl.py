#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: wuyue92tree@163.com

from string import Template


def change_project_name(name, path):
    f = open(path, 'r')
    t = Template(f.read()).substitute(project_name=name)

    return t


def change_spider_name(name, path):
    f = open(path, 'r')
    class_name = name.capitalize()
    spider_name = name
    t = Template(f.read()).substitute(class_name=class_name, spider_name=spider_name)
    return t

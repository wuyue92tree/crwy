#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: wuyue92tree@163.com

from string import Template

try:
    import ConfigParser
except ImportError:
    from configparser import ConfigParser


def get_project_name():
    conf = ConfigParser()
    conf.read('crwy.cfg', encoding='utf-8')
    project_name = conf.get('project', 'project_name').encode('utf-8')
    return project_name


def change_project_name(name, path):
    f = open(path, 'r')
    t = Template(f.read()).substitute(project_name=name)
    return t


def change_spider_name(name, path):
    f = open(path, 'r')
    class_name = name.capitalize()
    spider_name = name
    project_name = get_project_name()
    t = Template(f.read()).substitute(class_name=class_name, spider_name=spider_name, project_name=project_name)
    return t

#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: wuyue92tree@163.com

from string import Template


def change_project_name(name, path):
    f = open(path, 'r')
    t = Template(f.read()).substitute(project_name=name)

    return t

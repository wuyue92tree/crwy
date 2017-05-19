#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: wuyue92tree@163.com

from os.path import dirname, join
from setuptools import setup, find_packages

with open(join(dirname(__file__), 'crwy/VERSION'), 'rb') as f:
    version = f.read().decode('ascii').strip()

setup(
    name='Crwy',
    version=version,
    url='https://github.com/wuyue92tree/crwy',
    description='A Simple Web Crawling and Web Scraping framework',
    long_description=open('README.rst').read(),
    author='wuyue',
    author_email='wuyue92tree@163.com',
    maintainer='wuyue',
    maintainer_email='wuyue92tree@163.com',
    license='BSD',
    packages=find_packages(exclude=('tests', 'tests.*')),
    include_package_data=True,
    zip_safe=False,
    entry_points={
        'console_scripts': ['crwy = crwy.cmdline:execute']
    },
    install_requires=[
        'beautifulsoup4>=4.5.1',
        'requests==2.12.0',
        'configparser>=3.5.0',
        'SQLAlchemy>=1.0.14',
        'pyssdb>=0.1.2',
        'redis>=2.10.5',
        'gevent>=1.2.1'
    ],
)

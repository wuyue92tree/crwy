#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages
from crwy import version

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
    license='MIT',
    packages=find_packages(exclude=('tests', 'tests.*')),
    include_package_data=True,
    zip_safe=False,
    entry_points={
        'console_scripts': ['crwy = crwy.cmdline:execute']
    },
    install_requires=[
        'beautifulsoup4>=4.5.1',
        'requests>=2.20.0',
        'configparser>=3.5.0',
        'gevent>=1.2.1',
        'redis>=2.10.5,<3.0.0'
    ],
)

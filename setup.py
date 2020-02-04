#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages
from crwy import version

install_requires = []

with open('requirements.txt', 'r') as f:
    for req in f.readlines():
        install_requires.append(req.strip('\n'))


setup(
    name='Crwy',
    version=version,
    url='https://github.com/wuyue92tree/crwy',
    description='A Simple Web Crawling and Web Scraping framework',
    long_description=open('README.rst', encoding='utf-8').read(),
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
    install_requires=install_requires,
)

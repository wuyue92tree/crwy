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
    url='http://monkeyspace.cn',
    description='A Simple Web Crawling and Web Scraping framework',
    long_description=open('README.rst').read(),
    author='wuyue',
    maintainer='wuyue',
    maintainer_email='wuyue92tree@163.com',
    license='BSD',
    packages=find_packages(exclude=('tests', 'tests.*')),
    include_package_data=True,
    zip_safe=False,
    entry_points={
        'console_scripts': ['crwy = crwy.cmdline:execute']
    },
    classifiers=[
        'Framework :: Crwy',
        'Development Status :: Just Begin',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    install_requires=[
        'beautifulsoup4>=4.5.1',
        'pycurl>=7.43.0',
        'configparser>=3.5.0',
        'SQLAlchemy>=1.0.14',
    ],
)
Crwy
===================
.. image:: https://img.shields.io/pypi/v/Crwy.svg
   :target: https://pypi.python.org/pypi/Crwy
   :alt: PyPI Version
.. image:: https://travis-ci.org/wuyue92tree/crwy.svg?branch=1.0.2
   :target: https://travis-ci.org/wuyue92tree/crwy
   :alt: Build Status
.. image:: https://readthedocs.org/projects/crwy/badge/?version=1.0.2
   :target: http://crwy.readthedocs.io/zh_CN/1.0.2/?badge=1.0.2
   :alt: Documentation Status

简介
===================
Crwy是一个轻量级的爬虫抓取框架，参考Scrapy框架结构开发而来。该框架提供了实用的爬虫模板，旨在帮助大家快速实现爬虫任务，高效开发。

运行环境
===================

 * Python2.7
 * Works on Linux, Mac OSX

依赖包
===================
 * beautifulsoup4>=4.5.1
 * pycurl>=7.43.0
 * configparser>=3.5.0
 * SQLAlchemy>=1.0.14

安装
===================

快速安装::

    pip install crwy

or
前往下载: https://pypi.python.org/pypi/Crwy/1.0.2/

使用手册
===================
在这里: http://crwy.readthedocs.io/zh_CN/1.0.2/

友情链接
===================
- https://pypi.python.org/pypi/beautifulsoup4/
- https://pypi.python.org/pypi/pycurl/
- https://pypi.python.org/pypi/configparser/
- https://pypi.python.org/pypi/SQLAlchemy/

修改日志
===================
2017-01-09

- 修复模板中的BUG；
- 去除mysqldb依赖，用户根据自行需求进行安装；
- 讲utils中的sqlite包名称更改为db，且功能上更新为通用数据链接。


Crwy
====

|PyPI Version| |Download Status| |Build Status| |License Status|

简介
====

Crwy是一个轻量级的爬虫抓取框架，参考Scrapy框架结构开发而来。该框架提供了实用的爬虫模板，旨在帮助大家快速实现爬虫任务，高效开发。并为scrapy使用者提供通用轮子\ :sup:`.`\ 。新增了gevent，使爬虫异步执行，速度更快。

运行环境
========

-  Python2 & Python3
-  Works on Linux, Mac OSX

依赖包
======

-  beautifulsoup4>=4.5.1
-  requests>=2.20.0
-  configparser>=3.5.0
-  SQLAlchemy>=1.0.14
-  pyssdb>=0.1.2
-  redis>=2.10.5,<3.0.0
-  gevent>=1.2.1
-  retrying>=1.3.3
-  imapclient>=2.0.0

安装
====

快速安装

::

   pip install crwy

or 前往下载: https://pypi.python.org/pypi/Crwy/

使用手册
========

在这里: http://wuyue92tree.antio.top/opensource/crwy.html

友情链接
========

-  https://pypi.org/project/Scrapy/
-  https://pypi.org/project/selenium/
-  https://pypi.org/project/beautifulsoup4/
-  https://pypi.org/project/requests/
-  https://pypi.org/project/configparser/
-  https://pypi.org/project/SQLAlchemy/
-  https://pypi.org/project/gevent/
-  https://pypi.org/project/IMAPClient/

更新日志
========

http://wuyue92tree.antio.top/opensource/crwy.html#更新日志

TODO
====

-  完善scrapy_plugs
-  完善selenium_api
-  兼容python3

.. |PyPI Version| image:: https://img.shields.io/pypi/v/Crwy.svg
   :target: https://pypi.python.org/pypi/Crwy
.. |Download Status| image:: https://img.shields.io/pypi/dm/django-adminlte-ui.svg
   :target: https://pypi.python.org/pypi/Crwy
.. |Build Status| image:: https://travis-ci.org/wuyue92tree/crwy.svg
   :target: https://travis-ci.org/wuyue92tree/crwy
.. |License Status| image:: https://img.shields.io/github/license/wuyue92tree/crwy
   :target: https://raw.githubusercontent.com/wuyue92tree/crwy/master/LICENS

Crwy
===================
.. image:: https://img.shields.io/pypi/v/Crwy.svg
   :target: https://pypi.python.org/pypi/Crwy
   :alt: PyPI Version
.. image:: https://travis-ci.org/wuyue92tree/crwy.svg?branch=1.0.7
   :target: https://travis-ci.org/wuyue92tree/crwy
   :alt: Build Status
.. image:: https://readthedocs.org/projects/crwy/badge/?version=1.0.7
   :target: http://crwy.readthedocs.io/zh_CN/1.0.7/?badge=1.0.7
   :alt: Documentation Status

简介
===================
Crwy是一个轻量级的爬虫抓取框架，参考Scrapy框架结构开发而来。该框架提供了实用的爬虫模板，旨在帮助大家快速实现爬虫任务，高效开发。新增了gevent，使爬虫异步执行，速度更快。

运行环境
===================

 * Python2.7
 * Works on Linux, Mac OSX

依赖包
===================
 * beautifulsoup4>=4.5.1
 * requests==2.12.0
 * configparser>=3.5.0
 * SQLAlchemy>=1.0.14
 * pyssdb>=0.1.2
 * redis>=2.10.5
 * gevent>=1.2.1
 * IMAPClient>=1.0.2

安装
===================

快速安装::

    pip install crwy

or
前往下载: https://pypi.python.org/pypi/Crwy/1.0.7/

使用手册
===================
在这里: http://crwy.readthedocs.io/zh_CN/1.0.7/

友情链接
===================
- https://pypi.python.org/pypi/beautifulsoup4/
- https://pypi.python.org/pypi/requests/
- https://pypi.python.org/pypi/configparser/
- https://pypi.python.org/pypi/SQLAlchemy/
- https://pypi.python.org/pypi/gevent/
- https://pypi.python.org/pypi/IMAPClient/

修改日志
===================

2017-11-14  v1.0.7

- utils工具包中添加extend模块，用于添加第三方调用api;
- 升级mail包，改用imapclient接收解析邮件。

2017-09-21  v1.0.6

- 日志新增timedRtLogger模板及自定义Logger调用接口
- 爬虫执行脚本新增thread支持
- 修改项目创建脚本，配置文件固定在conf目录

2017-06-13  v1.0.5

- 解决pypi版本问题。

2017-06-12  v1.0.4

- 修改默认日志conf模板，RedisSet模块添加返回Set所有内容。

2017-06-01  v1.0.4

- 日志模块/邮件模块关联剥离。

2017-05-19  v1.0.4

- 下载器更换为requests, 并新增打文件下载方式;
- 新增RedisSet模块充当网页去重过滤器;
- 新增RedisHash模块，用于存储cookies等需持久化参数;
- 新增Logger模块，将默认日志集成到spider中，简化templates;
- 将内置的多进程启动更换为多协程，多进程直接由外部方式实现，框架不再支持;
- 优化templates。

2017-04-17  v1.0.3

- 修改下载器，支持自定义headers传入。

2017-04-04  v1.0.3

- 加入gevent，实现pycurl与gevent异步调用；
- 新增async异步模板；
- 修改HtmlDownloader返回值，返回Response对象。

2017-03-22  v1.0.2

- docs更新多进程，redis/ssdb队列文档。

2017-02-14  v1.0.2

- runspider模块新增多进程支持。

2017-02-07  v1.0.2

- 更改RedisQueue模块路径，新增SsdbQueue模块。

2017-01-09  v1.0.2

- 修复模板中的BUG；
- 去除mysqldb依赖，用户根据自行需求进行安装；
- 讲utils中的sqlite包名称更改为db，且功能上更新为通用数据链接。


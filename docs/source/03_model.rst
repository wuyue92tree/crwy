爬虫模板介绍
===================
basic模板
-------------------
basic模板包含最基本的抓取逻辑

* 下载: html_downloader
* 解析: html_parser

模板内容如下:
::

    #!/usr/bin/env python
    # -*- coding: utf-8 -*-

    from __future__ import print_function

    import logging
    import logging.config
    import pycurl
    import inspect
    from crwy.spider import Spider

    logging.config.fileConfig('./${project_name}/default_logger.conf')


    def get_current_function_name():
        return inspect.stack()[1][3]


    class ${class_name}Spider(Spider):
        def __init__(self):
            Spider.__init__(self)
            self.spider_name = '${spider_name}'
            self.logger = logging.getLogger('fileLogger')

        def crawler_${spider_name}(self):
            try:
                url = 'http://example.com'
                try:
                    html_cont = self.html_downloader.download(url)
                except pycurl.error:
                    self.logger.warning('%s : fail to access %s' % (get_current_function_name(), url))
                try:
                    soups = self.html_parser.parser(html_cont)
                except AttributeError:
                    self.logger.warning('%s : analysis fail on %s' % (get_current_function_name(), url))

                print(soups)
                self.logger.info('%s : crawler success !!!' % get_current_function_name())

            except Exception as e:
                    self.logger.error('%s : you got a error %s' % (get_current_function_name(), e))

        def run(self):
            self.crawler_${spider_name}()


可以看到,继承了一个名为Spider的类,该类中封装了html_downloader下载器和html_parser解析器,详情请阅读Utils详解中的Html章节。

sqlite模板
-------------------
sqlite模板将爬取数据存储到sqlite数据库中

* 下载: html_downloader
* 解析: html_parser
* 存储: sqlite

模板内容如下:
::

    #!/usr/bin/env python
    # -*- coding: utf-8 -*-

    from __future__ import print_function

    import logging
    import logging.config
    import pycurl
    import inspect
    from sqlalchemy import Integer, Column, String
    from crwy.spider import Spider
    from crwy.utils.sql.sqlite import Sqlite, Base

    logging.config.fileConfig('./${project_name}/default_logger.conf')


    def get_current_function_name():
        return inspect.stack()[1][3]


    class Test(Base):
        __tablename__ = "test"
        id = Column(Integer, primary_key=True, unique=True)
        title = Column(String(20))
        url = Column(String(20))


    class ${class_name}Spider(Spider):
        def __init__(self):
            Spider.__init__(self)
            self.spider_name = '${spider_name}'
            self.sql = Sqlite(database=self.spider_name)
            self.sql.init_table()
            self.logger = logging.getLogger('fileLogger')

        def crawler_${spider_name}(self):
            try:
                url = 'http://example.com'
                try:
                    html_cont = self.html_downloader.download(url)
                except pycurl.error:
                    self.logger.warning('%s : fail to access %s' % (get_current_function_name(), url))
                try:
                    soups = self.html_parser.parser(html_cont)
                except AttributeError:
                    self.logger.warning('%s : analysis fail on %s' % (get_current_function_name(), url))
                title = soups.find('title').text
                item = Test(title=title.decode('utf-8'), url=url.decode('utf-8'))
                self.sql.session.merge(item)
                self.sql.session.commit()
                print(soups)
                self.logger.info('%s : crawler success !!!' % get_current_function_name())

            except Exception as e:
                    self.logger.error('%s : you got a error %s' % (get_current_function_name(), e))

        def run(self):
            self.crawler_${spider_name}()


存储逻辑:

1. 通过创建class继承Base类(该类继承自sqlalchemy的declarative_base)生成table
2. 通过Sqlite类连接sqlite数据库,执行init_table()创建数据表, Sqlite类是什么 Click_ 。
3. 调用session.merge()存入相关数据,调用session.commit()使更改生效

.. _Click: 04_utils.html#sql

queue模板
-------------------
queue模块将待爬取页面加载到队列中,实时把控队列进度

* 寻找待爬取页面规则,将页面URL压入队列
* 从队列中取出一个URL
* 下载: html_downloader
* 解析: html_parser

模板内容如下:
::

    #!/usr/bin/env python
    # -*- coding: utf-8 -*-

    from __future__ import print_function

    import logging
    import logging.config
    import pycurl
    import inspect
    import Queue
    from crwy.spider import Spider

    logging.config.fileConfig('./${project_name}/default_logger.conf')

    queue = Queue.Queue()


    def get_current_function_name():
        return inspect.stack()[1][3]


    class ${class_name}Spider(Spider):
        def __init__(self):
            Spider.__init__(self)
            self.spider_name = '${spider_name}'
            self.logger = logging.getLogger('fileLogger')

        def crawler_${spider_name}(self):
            while True:
                try:
                    if not queue.empty():
                        url = 'http://example.com/%d' % queue.get()
                        try:
                            html_cont = self.html_downloader.download(url)
                        except pycurl.error:
                            self.logger.warning('%s : fail to access %s' % (get_current_function_name(), url))
                        try:
                            soups = self.html_parser.parser(html_cont)
                        except AttributeError:
                            self.logger.warning('%s : analysis fail on %s' % (get_current_function_name(), url))
                        print(url)
                        print('Length of queue : %d' % queue.qsize())
                    else:
                        self.logger.info('%s : crawler success !!!' % get_current_function_name())
                        exit()

                except Exception as e:
                    self.logger.error('%s : you got a error %s' % (get_current_function_name(), e))

        def run(self):
            for i in range(1, 10):
                queue.put(i)

            self.crawler_${spider_name}()


队列为多线程提供好的入口。

redis_queue模板
-------------------
redis_queue模板将队列持久化到redis服务器中,以解决服务器宕机导致任务丢失的问题

* 连接redis服务器: RedisQueue, 新建队列
* 寻找待爬取页面规则,将页面URL压入队列
* 从队列中取出一个URL
* 下载: html_downloader
* 解析: html_parser

模板内容如下:
::

    #!/usr/bin/env python
    # -*- coding: utf-8 -*-

    from __future__ import print_function

    import logging
    import logging.config
    import pycurl
    import inspect
    import sys
    from crwy.spider import Spider
    from crwy.RedisQueue import RedisQueue

    logging.config.fileConfig('./${project_name}/default_logger.conf')

    queue = RedisQueue('foo')


    def get_current_function_name():
        return inspect.stack()[1][3]


    class ${class_name}Spider(Spider):
        def __init__(self):
            Spider.__init__(self)
            self.spider_name = '${spider_name}'
            self.logger = logging.getLogger('fileLogger')

        def crawler_${spider_name}(self):
            while True:
                try:
                    if not queue.empty():
                        url = 'http://example.com/%d' % queue.get()
                        try:
                            html_cont = self.html_downloader.download(url)
                        except pycurl.error:
                            self.logger.warning('%s : fail to access %s' % (get_current_function_name(), url))
                        try:
                            soups = self.html_parser.parser(html_cont)
                        except AttributeError:
                            self.logger.warning('%s : analysis fail on %s' % (get_current_function_name(), url))
                        print(url)
                        print('Length of queue : %d' % queue.qsize())
                    else:
                        self.logger.info('%s : crawler success !!!' % get_current_function_name())
                        exit()

                except Exception as e:
                    self.logger.error('%s : you got a error %s' % (get_current_function_name(), e))

        def add_queue(self):
            for i in range(1, 10):
                queue.put(i)

        def run(self):
            try:
                worker = sys.argv[4]
            except :
                print 'No worker found!!!\n'

            if worker == 'crawler':
                self.crawler_${spider_name}()
            else:
                self.add_queue()

添加add_queue()方法,可实现在程序不中断的情况下,继续添加新的抓取目标。

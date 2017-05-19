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

    from crwy.spider import Spider


    class ${class_name}Spider(Spider):
        def __init__(self):
            Spider.__init__(self)
            self.spider_name = '${spider_name}'

        def crawler_${spider_name}(self):
            try:
                url = 'http://example.com'
                response = self.html_downloader.download(url)
                soups = self.html_parser.parser(response.content)
                print(url)
                print(soups)
                self.logger.info('%s[%s] --> %s : crawler success !!!' % (
                    self.spider_name, self.worker, self.func_name()))

            except Exception as e:
                self.logger.exception('%s[%s] --> %s : %s' % (
                    self.spider_name, self.worker,
                    self.func_name(), e))

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

    from sqlalchemy import Integer, Column, String
    from crwy.spider import Spider
    from crwy.utils.sql.db import Database, Base


    class Test(Base):
        __tablename__ = "test"
        id = Column(Integer, primary_key=True, unique=True)
        title = Column(String(20))
        url = Column(String(20))


    class ${class_name}Spider(Spider):
        def __init__(self):
            Spider.__init__(self)
            self.spider_name = '${spider_name}'
            self.sql = Database('sqlite:///./data/test.db')
            self.sql.init_table()

        def crawler_${spider_name}(self):
            try:
                url = 'http://example.com'
                response = self.html_downloader.download(url)
                soups = self.html_parser.parser(response.content)
                title = soups.find('title').text
                item = Test(title=title.decode('utf-8'), url=url.decode('utf-8'))
                self.sql.session.merge(item)
                self.sql.session.commit()
                print(url)
                print(soups)
                self.logger.info('%s[%s] --> %s : crawler success !!!' % (
                    self.spider_name, self.worker, self.func_name()))

            except Exception as e:
                self.logger.exception('%s[%s] --> %s : %s' % (
                    self.spider_name, self.worker,
                    self.func_name(), e))

        def run(self):
            self.crawler_${spider_name}()



存储逻辑:

1. 通过创建class继承Base类(该类继承自sqlalchemy的declarative_base)生成table
2. 通过Database类连接sqlite数据库,执行init_table()创建数据表, Sqlite类是什么 Click_ 。
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

    import sys
    import Queue
    from crwy.spider import Spider

    queue = Queue.Queue()


    class ${class_name}Spider(Spider):
        def __init__(self):
            Spider.__init__(self)
            self.spider_name = '${spider_name}'

        def crawler_${spider_name}(self):
            while True:
                try:
                    if not queue.empty():
                        url = 'http://example.com/%d' % queue.get()
                        response = self.html_downloader.download(url)
                        soups = self.html_parser.parser(response.content)
                        print(url)
                        print(soups)
                        print('Length of queue : %d' % queue.qsize())
                    else:
                        self.logger.info('%s[%s] --> %s : crawler success !!!' % (
                            self.spider_name, self.worker, self.func_name()))
                        sys.exit()

                except Exception as e:
                    self.logger.exception('%s[%s] --> %s : %s' % (
                        self.spider_name, self.worker,
                        self.func_name(), e))
                    continue

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

    import sys
    from crwy.spider import Spider
    from crwy.utils.queue.RedisQueue import RedisQueue
    from crwy.utils.filter.RedisSet import RedisSet


    queue = RedisQueue('foo')
    s_filter = RedisSet('foo')


    class ${class_name}Spider(Spider):
        def __init__(self):
            Spider.__init__(self)
            self.spider_name = '${spider_name}'

        def crawler_${spider_name}(self):
            while True:
                try:
                    if not queue.empty():
                        url = 'http://example.com/%s' % queue.get()
                        if s_filter.sadd(url) is False:
                            print('You got a crawled url. %s' % url)
                            continue
                        response = self.html_downloader.download(url)
                        soups = self.html_parser.parser(response.content)
                        print(url)
                        print(soups)
                        print('Length of queue : %s' % queue.qsize())
                    else:
                        self.logger.info('%s[%s] --> %s : crawler success !!!' % (
                            self.spider_name, self.worker, self.func_name()))
                        sys.exit()

                except Exception as e:
                    self.logger.exception('%s[%s] --> %s : %s' % (
                        self.spider_name, self.worker,
                        self.func_name(), e))
                    continue

        def add_queue(self):
            for i in range(100):
                queue.put(i)
            print(queue.qsize())

        def run(self):
            try:
                worker = sys.argv[4]
            except :
                print('No worker found!!!\n')
                sys.exit()

            if worker == 'crawler':
                self.crawler_${spider_name}()
            elif worker == 'add_queue':
                self.add_queue()
            elif worker == 'clean':
                queue.clean()
                s_filter.clean()
            else:
                print('Invalid worker <%s>!!!\n' % worker)



添加add_queue()方法,可实现在程序不中断的情况下,继续添加新的抓取目标。

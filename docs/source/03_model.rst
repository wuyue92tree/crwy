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

        def crawler_${spider_name}(self):
            url = 'http://example.com'
            html_cont = self.html_downloader.download(url)
            soups = self.html_parser.parser(html_cont)
            print(soups)


    def main():
        run=${class_name}Spider()
        run.crawler_${spider_name}()

    if __name__ == '__main__':
        main()

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

    from crwy.spider import Spider
    from crwy.utils.sql.sqlite import *


    class Test(Base):
        __tablename__ = "test"
        id = Column(Integer, primary_key=True, unique=True)
        title = Column(String(20))
        url = Column(String(20))


    class ${class_name}Spider(Spider):
        def __init__(self):
            Spider.__init__(self)
            self.sql = Sqlite('${spider_name}')
            self.sql.init_table()

        def crawler_${spider_name}(self):
            url = 'http://example.com'
            html_cont = self.html_downloader.download(url)
            soups = self.html_parser.parser(html_cont)
            title = soups.find('title').text
            item = Test(title=title.decode('utf-8'), url=url.decode('utf-8'))
            self.sql.session.merge(item)
            self.sql.session.commit()
            print(soups)

    def main():
        run=${class_name}Spider()
        run.crawler_${spider_name}()

    if __name__ == '__main__':
        main()

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

    import Queue
    from crwy.spider import Spider
    from crwy.RedisQueue import RedisQueue

    queue = Queue.Queue()


    class ${class_name}Spider(Spider):
        def __init__(self, queue):
            Spider.__init__(self)
            self.queue = queue

        def crawler_${spider_name}(self):
            while True:
                if not queue.empty():
                    url = 'http://example.com/%d' % self.queue.get()
                    html_cont = self.html_downloader.download(url)
                    soups = self.html_parser.parser(html_cont)
                    print(url)
                    print('Length of queue : %d' % queue.qsize())
                else:
                    return False

    def main():
        for i in range(1, 10):
            queue.put(i)

        run = ${class_name}Spider(queue)
        run.crawler_${spider_name}()


    if __name__ == '__main__':
        main()

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

    from optparse import OptionParser
    from crwy.spider import Spider
    from crwy.RedisQueue import RedisQueue

    queue = RedisQueue('test')


    class ${class_name}Spider(Spider):
        def __init__(self, queue):
            Spider.__init__(self)
            self.queue = queue

        def crawler_${spider_name}(self):
            while True:
                url = 'http://example.com/%d' % int(self.queue.get())
                html_cont = self.html_downloader.download(url)
                soups = self.html_parser.parser(html_cont)
                print(url)
                print('Length of queue : %d' % queue.qsize())

    def crawler():
        run=${class_name}Spider(queue)
        run.crawler_${spider_name}()

    def add_queue():
        for i in range(1, 10):
            queue.put(i)

    if __name__ == '__main__':
        Usage = "Usage:  python ${spider_name}.py <commands>"
        parser = OptionParser(Usage)
        opt, args = parser.parse_args()
        if len(args) < 1:
            print(Usage)
            exit()

        if args[0] == 'crawler':
            crawler()
        if args[0] == 'queue':
            add_queue()

添加add_queue()方法,可实现在程序不中断的情况下,继续添加新的抓取目标。

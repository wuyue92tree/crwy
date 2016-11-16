补充内容
===================
RedisQueue
-------------------

如何优雅的将redis当成消息队列

- __init__(name, namespace='queue', \*\*redis_kwargs)

 | name: 队列名称
 | namespace: 命名空间(默认为queue)
 | \*\*redis_kwargs: redis模块初始化参数

- qsize()
    返回队列长度

- empty()
    队列为空时返回True

- put()
    向队列中压入一条数据

- get()
    从队列中取出一条数据

- get_nowait()
    从队列中取出一条数据，不阻塞

- clean()
    清空队列


代码如下：
::

    #!/usr/bin/env python
    # -*- coding: utf-8 -*-
    # author: wuyue92tree@163.com

    import redis


    class RedisQueue(object):
        """Simple Queue with Redis Backend"""

        def __init__(self, name, namespace='queue', **redis_kwargs):
            """The default connection parameters are: host='localhost', port=6379, db=0"""
            self.__db = redis.Redis(**redis_kwargs)
            self.key = '%s:%s' % (namespace, name)

        def qsize(self):
            """Return the approximate size of the queue."""
            return self.__db.llen(self.key)

        def empty(self):
            """Return True if the queue is empty, False otherwise."""
            return self.qsize() == 0

        def put(self, item):
            """Put item into the queue."""
            self.__db.rpush(self.key, item)

        def get(self, block=True, timeout=None):
            """Remove and return an item from the queue.

            If optional args block is true and timeout is None (the default), block
            if necessary until an item is available."""
            if block:
                item = self.__db.blpop(self.key, timeout=timeout)
            else:
                item = self.__db.lpop(self.key)

            if item:
                item = item[1]
            return item

        def get_nowait(self):
            """Equivalent to get(False)."""
            return self.get(False)

        def clean(self):
            """Empty key"""
            return self.__db.delete(self.key)

日志系统
-------------------
日志采用配置文件的形式工作

eg: default_logger.conf
::

    #logger.conf
    ###############################################
    [loggers]
    keys=root,fileLogger,rtLogger

    [logger_root]
    level=INFO
    handlers=consoleHandler

    [logger_fileLogger]
    handlers=consoleHandler,fileHandler
    qualname=fileLogger
    propagate=0

    [logger_rtLogger]
    handlers=consoleHandler,rtHandler
    qualname=rtLogger
    propagate=0

    ###############################################
    [handlers]
    keys=consoleHandler,fileHandler,rtHandler

    [handler_consoleHandler]
    class=StreamHandler
    level=INFO
    formatter=simpleFmt
    args=(sys.stderr,)

    [handler_fileHandler]
    class=FileHandler
    level=DEBUG
    formatter=defaultFmt
    args=('./log/default.log', 'a')

    [handler_rtHandler]
    class=handlers.RotatingFileHandler
    level=DEBUG
    formatter=defaultFmt
    args=('./log/default.log', 'a', 10*1024*1024, 5)

    ###############################################

    [formatters]
    keys=defaultFmt,simpleFmt

    [formatter_defaultFmt]
    format=%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s
    datefmt=%a, %d %b %Y %H:%M:%S

    [formatter_simpleFmt]
    format=%(name)-12s: %(levelname)-8s %(message)s
    datefmt=


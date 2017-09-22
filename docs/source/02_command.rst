命令行工具介绍
===================
开始
-------------------
在终端中键入: crwy, 将在屏幕上看到如下显示
::

    Crwy - no active project found!!!

    Usage:
      crwy <commands> [option] [args]

    Avaliable Commands:
      list 		list all spider in your project
      runspider    	run a spider
      startproject 	create a new project
      createspider 	create a new spider
      version      	show version

    Use "crwy <command> -h" to see more info about a command

可以看到crwy支持list, runspider, startproject, createspider等命令,想知道它们都是怎么用的么?继续往下看吧。

startproject
-------------------
该命令用以新建爬虫项目
::

    crwy startproject spidertest

执行成功会得到如下返回:
::

    Project start......enjoy^.^

那么该命令到底干了些什么呢?
::

    spidertest
    ├── crwy.cfg            确认项目名称及settings所在目录
    ├── data                爬取结果存储目录(sqlite存储的默认路径)
    │   ├── __init__.py
    │   └── __init__.pyc
    ├── spidertest
    │   └── settings.py     项目配置文件
    └── src                 爬虫所在目录
        ├── __init__.py
        └── __init__.pyc

它建立了一个名为: spidertest的工程, 里面包含了爬虫将用到的配置(将在后面详细解释)。

createspider
-------------------
该命令用以新建爬虫
添加"-h"参数,看该命令如何使用:
::

    crwy createspider -h

执行成功会得到如下返回:
::

    Usage:  crwy createspider [option] [args]

    Options:
      -h, --help            show this help message and exit
      -l, --list            list available spider template name
      -p PREVIEW, --preview=PREVIEW
                            preview spider template
      -t TEMPLATE, --tmpl=TEMPLATE
                            spider template
      -n NAME, --name=NAME  new spider name

* -l: 用以列举可用的爬虫模板
* -p: 用以查看模板代码
* -t: 用以指定继承的模板名称
* -n: 用以指定将要创建的爬虫的名称

例子:
::

    crwy createspider -t basic -n basictest

便可在src目录中找到生成的相对应的爬虫程序
注意: 创建爬虫时需在项目根目录下(即:crwy.cfg文件所在目录),否则项目将创建失败。

list
-------------------
该命令用以显示爬虫列表
::

    crwy list

runspider
-------------------
该命令用以执行爬虫

添加"-h"参数,看该命令如何使用:
::

    crwy runspider -h

::


    Usage:  crwy runspider [option] [args]

    Options:
      -h, --help            show this help message and exit
      -n NAME, --name=NAME  spider name
      -c COROUTINE, --coroutine=COROUTINE
                            crawler by multi coroutine
      -t THREAD, --thread=THREAD
                            crawler by multi thread



* -n: 用以指定将要执行的爬虫的名称
* -c: 用以控制程序采用多协程运行（-c参数后接协程数）
* -t: 用以控制程序采用多协程运行（-t参数后接线程数）

version
-------------------
该命令用以查看crwy版本号
::

    crwy version



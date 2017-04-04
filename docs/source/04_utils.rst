Utils详解
===================
Html
-------------------
html_downloader
>>>>>>>>>>>>>>>>>>>

采用Pycurl做为下载器引擎

- download(url, method='GET', postdata=None, proxy=None, cookie=None, cookiefile=None, cookiejar=None, debug=False, autoclose=True, useragent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:46.0) Gecko/20100101 Firefox/46.0', referer='http://spider.wuyue.tk', FOLLOWLOCATION=1, MAXREDIRS=5, TIMEOUT=600)

 | url: 目标网站URL
 | method: 规定请求方式，默认为GET
 | postdata: 请求方式为POST时，post表单的内容(类型应该为dict)
 | proxy: 是否采用代理进行请求(默认为空, 类型为list)
 | cookie: 指定Cookie
 | cookiefile: 指定Cookiefile
 | cookiejar: 指定Cookiejar
 | debug: 开启pycurl调试模式(默认为False)
 | autoclose: 是否自动关闭连接(默认为True)
 | useragent: 指定请求useragent， 默认为：'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:46.0) Gecko/20100101 Firefox/46.0'
 | referer: 指定请求referer， 默认为：'http://spider.wuyue.tk'
 | FOLLOWLOCATION: 是否开启自动跳转(默认为1)
 | MAXREDIRS: 规定最大跳转次数(默认为5)
 | TIMEOUT: 规定超时时间(默认为600)

- close()
    关闭连接

pycurl传送门: http://pycurl.io/

html_parser
>>>>>>>>>>>>>>>>>>>

采用BeautifulSoup4做为解析器引擎

- parser(response)

 | 解析UTF-8编码网页

- gbk_parser(response)

 | 解析GBK编码网页

- jsonp_parser(response)

 | 解析不规则json网页(key不带双引号),返回dict


beautifulsoup4传送门: https://www.crummy.com/software/BeautifulSoup/

Sql
-------------------
db
>>>>>>>>>>>>>>>>>>>

采用sqlalchemy操作数据库
具体支持数据库，参考：http://docs.sqlalchemy.org/en/latest/core/engines.html

- __init__(db_url, \*\*kwargs)

 | db_url为数据库地址

- init_table()

 | 初始化数据库

- drop_table()

 | 清空数据库

sqlalchemy传送门: http://www.sqlalchemy.org/

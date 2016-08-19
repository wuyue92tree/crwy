Utils详解
===================
Html
-------------------
html_downloader
>>>>>>>>>>>>>>>>>>>

采用Pycurl做为下载器引擎

- download(url, Gzip=False, Proxy=None, Cookie=None)

 | url: 目标网站URL
 | Gzip: 网站返回值,是否通过Gzip压缩(默认为False)
 | Proxy: 是否采用代理进行请求(默认为空)
 | Cookie: 是否指定Cookie

pycurl传送门: http://pycurl.io/

html_parser
>>>>>>>>>>>>>>>>>>>

采用BeautifulSoup4做为解析器引擎

- parser(html_cont)

 | 解析UTF-8编码网页

- gbk_parser(html_cont)

 | 解析GBK编码网页

- jsonp_parser(html_cont)

 | 解析不规则json网页(key不带双引号),返回dict

- get_parser_urls(html_cont)

 | 获取html_cont中所有链接


beautifulsoup4传送门: https://www.crummy.com/software/BeautifulSoup/

Sql
-------------------
sqlite
>>>>>>>>>>>>>>>>>>>

采用sqlalchemy操作sqlite数据库

- __init__(database)

 | database为生成数据库的名称

- init_table()

 | 初始化数据库

- drop_table()

 | 清空数据库

sqlalchemy传送门: http://www.sqlalchemy.org/

mysql
>>>>>>>>>>>>>>>>>>>
开发中。。。。。。
Utils详解
===================
Html
-------------------
html_downloader
>>>>>>>>>>>>>>>>>>>

采用requests做为下载器引擎

本框架采用版本 2.12.0

- download(url, method='GET', timeout=60)

 | url: 目标网站URL
 | method: 规定请求方式，默认为GET
 | timeout: 规定超时时间(默认为60)
 | **kwargs: 与requests保持一致

- downloadFile(url, save_path='./data/')

 | url: 目标文件URL
 | save_path: 文件保存路径

requests传送门: http://www.python-requests.org/en/master/

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

Utils详解
===================
Html
-------------------
html_downloader
>>>>>>>>>>>>>>>>>>>

采用Pycurl做为下载器引擎

- download(url, method='GET', postdata=None, proxy=None, cookie=None, cookiefile=None, cookiejar=None, Gzip=False, debug=False, autoclose=True, FOLLOWLOCATION=1, MAXREDIRS=5, TIMEOUT=600)

 | url: 目标网站URL
 | method: 规定请求方式，默认为GET
 | postdata: 请求方式为POST时，post表单的内容(类型应该为dict)
 | proxy: 是否采用代理进行请求(默认为空, 类型为list)
 | cookie: 指定Cookie
 | cookiefile: 指定Cookiefile
 | cookiejar: 指定Cookiejar
 | Gzip: 网站返回值,是否通过Gzip压缩(默认为False)
 | debug: 开启pycurl调试模式(默认为False)
 | autoclose: 是否自动关闭连接(默认为True)
 | FOLLOWLOCATION: 是否开启自动跳转(默认为1)
 | MAXREDIRS: 规定最大跳转次数(默认为5)
 | TIMEOUT: 规定超时时间(默认为600)

- get_header()
    返回请求头信息

- get_http_conn_time()
    返回服务器响应时间

- get_http_total_time()
    返回请求总用时

- get_response_code()
    返回状态码

- close()
    关闭连接

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

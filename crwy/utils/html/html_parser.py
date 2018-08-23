# -*- coding: utf-8 -*-

import sys
from bs4 import BeautifulSoup
try:
    import PyV8
except ImportError:
    pass


class HtmlParser(object):
    """ 解析器 """
    @staticmethod
    def parser(response):
        """
        utf-8字符处理
        :param response: 待处理字符串
        :return: 返回bs对象
        """
        if response is None:
            return

        if sys.version_info < (3, ):
            soup = BeautifulSoup(str(response), 'html.parser',
                                 from_encoding='utf-8')
        else:
            soup = BeautifulSoup(str(response), 'html.parser')

        return soup

    @staticmethod
    def gbk_parser(response):
        """
        gbk字符处理
        :param response: 待处理字符串
        :return: 返回bs对象
        """
        if response is None:
            return

        if sys.version_info < (3, ):
            soup = BeautifulSoup(str(response), 'html.parser',
                                 from_encoding='gb18030')
        else:
            soup = BeautifulSoup(str(response), 'html.parser')

        return soup

    @staticmethod
    def jsonp_parser(data):
        """
        非规范json数据处理 {a:1, b:1}
        key非字符串
        :param data: 待处理字符串
        :return: 返回标准json数据
        """
        ctx = PyV8.JSContext()
        ctx.enter()
        ctx.eval("""
            function func() {
              var data = """ + data + """;
              var json_data = JSON.stringify(data);
              return json_data;
            }
        """)
        return ctx.locals.func()


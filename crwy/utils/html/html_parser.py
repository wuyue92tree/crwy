# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
try:
    from pyv8 import PyV8
except ImportError:
    pass


class HtmlParser(object):
    """ 解析器 """
    def parser(self, response):
        """
        utf-8字符处理
        :param response: 待处理字符串
        :return: 返回bs对象
        """
        if response is None:
            return

        soup = BeautifulSoup(str(response), 'html.parser',
                             from_encoding='utf-8')

        return soup

    def gbk_parser(self, response):
        """
        gbk字符处理
        :param response: 待处理字符串
        :return: 返回bs对象
        """
        if response is None:
            return

        soup = BeautifulSoup(str(response), 'html.parser',
                             from_encoding='gb18030')

        return soup

    def jsonp_parser(self, data):
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


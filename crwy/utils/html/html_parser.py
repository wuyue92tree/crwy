# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
# from pyv8 import PyV8


class HtmlParser(object):
    def parser(self, html_cont):
        if html_cont is None:
            return

        soup = BeautifulSoup(str(html_cont), 'html.parser', from_encoding='utf-8')

        return soup

    def gbk_parser(self, html_cont):
        if html_cont is None:
            return

        soup = BeautifulSoup(str(html_cont), 'html.parser', from_encoding='gb18030')

        return soup

    def jsonp_parser(self, data):
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


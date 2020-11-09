#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: wuyue
@contact: wuyue92tree@163.com
@software: IntelliJ IDEA
@file: font_analysis.py
@create at: 2018-08-22 19:42

这一行开始写关于本文件的说明与解释

本工具类适用于58同城，其他站点可将该类作为基础类进行扩展

思路：

1. 获取web页面内容；
2. 获取字体文件；
3. 获取字体xml文件，解析出经过自定义的文字；
4. 获取文字value的hash值（经测试发现，文字的key、value对应关系每次请求都是变化的，而不可能
改变的是字的value，所以这里通过文字value的hash值来确定，是哪一个字，反推确定页面上的字符对应的
字是什么。）

like：

'77880914931fb6dda97269a9156404745f609d35': '黄'

hash值与文字对应mapping需要人工，通过字体软件对应 推荐 fontforge

5. 通过人工确认的mapping，找到页面上字符与真实字体的对应关系；
6. 替换原始页面中的字符

"""

import base64
import hashlib
# import json
import os
import re
import uuid
from fontTools.ttLib import TTFont
from crwy.spider import BaseSpider


class FontAnalysis(BaseSpider):
    def __init__(self, html=None):
        super(FontAnalysis, self).__init__()
        uid = str(uuid.uuid1())
        self.font_path = './data/font/font-{}.woff'.format(uid)
        self.xml_path = './data/xml/font-{}.xml'.format(uid)
        self.html = html if html else self.get_test_html()

    def get_test_html(self):
        # 58简历页
        url = 'https://bj.58.com/qzyewu/pn2/?PGTID=0d303353-0000-1188-7c8a-829b2b71d0e8&ClickID=2'

        res = self.html_downloader.download(url)

        return res.text

    def save_font(self):
        """
        保存字体
        :return:
        """
        base64string = re.search('(?<=base64,).*?(?=\))', self.html).group()
        bin_data = base64.b64decode(base64string)
        with open(self.font_path, 'wb') as f:
            f.write(bin_data)

    def get_font_xml(self):
        """
        获取字体 xml
        :return:
        """
        font = TTFont(self.font_path)
        font.saveXML(self.xml_path)

    def analysis(self, is_clean=True, debug=False):
        """
        解析xml，获取web页面字符与文字key及文字value hash值的对应关系
        :param is_clean: 是否清楚字体文件及字体xml文件
        :param debug: 是否终端输出字体对照关系
        :return:
        """

        self.save_font()
        self.get_font_xml()
        with open(self.xml_path, 'rb') as xml:
            soups = self.html_parser.parser(xml.read())
            ttglyph_lst = soups.find('glyf').find_all('ttglyph')[1:]
            map_lst = soups.find('cmap').find_all('map')
            map_dict = {}
            for map in map_lst:
                map_dict[map.get('name')] = map.get('code')
            # print(map_dict, len(map_dict))
            analysis_res = []
            for ttglyph in ttglyph_lst:
                analysis_dict = dict()
                analysis_dict['ttglyph_name'] = ttglyph.get('name')
                # analysis_dict['html_name'] = '&#x{};'.format(
                #     analysis_dict['ttglyph_name'][3:].lower())
                # x_distance = str(int(ttglyph.get('xmax')) - int(ttglyph.get('xmin')))
                # y_distance = str(int(ttglyph.get('ymax')) - int(ttglyph.get('ymin')))
                analysis_dict['html_name'] = '&#x{};'.format(
                    map_dict.get(ttglyph.get('name'))[2:].upper())
                ttglyph_value = []
                contour_lst = ttglyph.find_all('contour')
                for contour in contour_lst:
                    pt_lst = contour.find_all('pt')
                    for pt in pt_lst[:1]:
                        tmp = str(int(pt.get('x')) - int(pt.get('y')))
                        # pt['y'] = str(int(y_distance) - int(pt.get('y')))
                        ttglyph_value.append(tmp)
                analysis_dict['ttglyph_value'] = str(sorted(ttglyph_value))
                analysis_dict['font_hash'] = hashlib.sha1(
                    analysis_dict['ttglyph_value'].encode('utf-8')
                ).hexdigest()
                analysis_res.append(analysis_dict)

                if debug:
                    print(analysis_dict['ttglyph_name'],  # 字体key
                          analysis_dict['html_name'],  # web页面显示值
                          analysis_dict['font_hash'],  # 字体内容哈希值
                          analysis_dict['ttglyph_value'])

            if is_clean:
                os.remove(self.font_path)
                os.remove(self.xml_path)

            return analysis_res

    @staticmethod
    def get_real_font_mapping(analysis_res, font_mapping, debug=False):
        real_font_mapping = dict()
        for item in analysis_res:
            real_font_mapping[item['html_name']] = font_mapping[
                item['font_hash']]
            if debug is True:
                print(item['html_name'], font_mapping[item['font_hash']])

        return real_font_mapping

    @staticmethod
    def recover_html(html, real_font_mapping):
        for k, v in real_font_mapping.items():
            html = html.replace(k, v)
        return html


font_mapping = {
    '7fd63556d48347cd5a50007b3151e2735f93bed2': '',
    'ed465eefa32423091781b4cf7136d16d3ebce463': '技',
    'f9e740d4af46806fd75ab69783555c87f6ec7706': '6',
    '50365252b61dbe2651e0c83bebc8d00ef763a158': '经',
    'ecc7ed15aa268e5a699eb8ddbe73ad2b27911ee1': '王',
    '891090dd6e752593d367a61dc3891f1cb110f0dc': '应',
    '6aea2037fa2d83b11da6dcc837443c7b2a9be22e': '专',
    '7138fba5e0f9093c696c20ac994857385f257c1e': '赵',
    '2609770c8afd922eb37758dd8828db1b566c7fd6': '李',
    '02c3341d2d8085eded8233ece3f54b6540322eac': '以',
    '75859289bdf9b78f1842ed692daf445f403e2b88': '吴',
    'f9dcd3c88958fc85f6fbf770532929d3b3891a53': '女',
    'e83dc230a3f59d5361bbcdc82973529c6fcbf443': '杨',
    '8371e4d560301720541aa2b18c92d7624ff11082': '7',
    '19abe86dc73d03989b6e2c9ba3e86d05f187a3c6': '5',
    'fdb060ded208610d1923ff00a5cee237a021be83': '张',
    'b032add2a6287c5d6ab051bef17e37c45d714f40': 'B',
    '5b262e3ff34a8ec29d9b5b271e0de2396de260ce': '本',
    '512adeb01f06bca832fd2a6dea974f09029edeeb': '男',
    '6f15d67b48b66a140ca1858aae74897c4a5a79f6': '博',
    'b2f5589957afac462f1620e6647e7c33f05dce96': '3',
    'e24ed92db7331e919161e6d2961d35ccaae0593a': '无',
    '3cd650e51bbe8268ffb4ec2ab9537937eddac0dd': '9',
    'e1eb5abd0f77e1c2627a50eda8a4765c4be7a606': '生',
    '04783616ad232d7ad4d886876f4eaaf5a0bbb580': '验',
    '374446ca738266d7c1da2a551f15c54cdd12e460': '8',
    'e2af36b0e0add44124e65c78e0bb388a91da5373': '下',
    '679f2fd459c646e6e1668938a57f7c1a248f806d': '科',
    '6924fddd64c781721e91d3797742761616b58532': '1',
    'c81c0fe74c783fdc90d8ff7bcb801ac73646f5bf': '4',
    '07aa1ed8e3c9b283fd20a9942fd81d925fb49de2': 'M',
    '968f86f893ff4e01575e3acc1e61c940b424d479': '中',
    '7b9ef322a4ea16ddd46ce3afbf9ae7265b638947': '硕',
    '5ac2c4226b898a1cb133c1cd012506399c291253': '届',
    'e51700563d6f6c7c82def8c408b972ae28870a7e': '2',
    '44b8aeb98a4556a2d9e0121848d1ce5ddd1cf820': '刘',
    'b1df1706be1e25ce632329d0967bc4d87de7a0ce': '士',
    'b412e5268df2f25d418a5547c902e0794ed33a7c': '陈',
    'c0fdac37111eee42dde8f1481eddf803c1c6eafd': '高',
    '859502b5860c99ec88061eb60dfc0c2af03e1778': '大',
    'afd6a61616dbb4215b9327194e177e6caa71ace9': '0',
    'f4d6418264b302bc9d70693b5cc3d4a7da01a445': 'E',
    'b74117c62c7ff7ae79a1d01dfe0baa21874d3ae8': '周',
    '9372bfdc75a272eceb0f4fbf8bd5c86bc21b4b1d': 'A',
    '9e2c166141627880782747ba69b9972885ca798a': '校',
    'f38c4fe982d55a9bcb4460b82db43f995bc5a992': '黄'
}

# def main():
#     runner = FontAnalysis()
#     analysis_res = runner.analysis(debug=True)
#     real_font_mapping = runner.get_real_font_mapping(analysis_res, font_mapping)
#     print(real_font_mapping)
#
#     real_html = runner.recover_html(html=runner.html,
#                                     real_font_mapping=real_font_mapping)
#     print(real_html)
#
#
# if __name__ == '__main__':
#     main()

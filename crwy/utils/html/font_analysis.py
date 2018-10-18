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
import json
import os
import re
import uuid
from fontTools.ttLib import TTFont
from crwy.spider import Spider


class FontAnalysis(Spider):
    def __init__(self, html=None):
        super(FontAnalysis, self).__init__()
        uid = str(uuid.uuid1())
        self.font_path = './data/font/font-{}.woff'.format(uid)
        self.xml_path = './data/xml/font-{}.xml'.format(uid)
        self.html = html if html else self.get_test_html()

    def get_test_html(self):
        # 58简历页
        url = 'https://bj.58.com/qzyewu/pn2/?' \
              'PGTID=0d303353-0000-1188-7c8a-829b2b71d0e8&ClickID=2'

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
            analysis_res = []
            for ttglyph in ttglyph_lst:
                analysis_dict = dict()
                analysis_dict['ttglyph_name'] = ttglyph.get('name')
                analysis_dict['html_name'] = '&#x{};'.format(
                    analysis_dict['ttglyph_name'][3:].lower())
                ttglyph_value = []
                contour_lst = ttglyph.find_all('contour')
                for contour in contour_lst:
                    pt_lst = contour.find_all('pt')
                    for pt in pt_lst:
                        ttglyph_value.append(pt.attrs)
                analysis_dict['font_hash'] = hashlib.sha1(
                    json.dumps(ttglyph_value, sort_keys=True).encode(
                        'utf-8')).hexdigest()
                analysis_res.append(analysis_dict)

                if debug:
                    print(analysis_dict['ttglyph_name'],  # 字体key
                          analysis_dict['html_name'],  # web页面显示值
                          analysis_dict['font_hash'])  # 字体内容哈希值

            if is_clean:
                os.remove(self.font_path)
                os.remove(self.xml_path)

            return analysis_res

    @staticmethod
    def get_real_font_mapping(analysis_res, font_mapping):
        real_font_mapping = dict()
        for item in analysis_res:
            real_font_mapping[item['html_name']] = font_mapping[
                item['font_hash']]
        return real_font_mapping

    @staticmethod
    def recover_html(html, real_font_mapping):
        for k, v in real_font_mapping.items():
            html = html.replace(k, v)
        return html


font_mapping = {
    '275e74d6bddd35d10b983741abfc488c1edeba55': '技',
    '8cc5efb98e3e8f3cd7c5349a081a8a5c4584ff9b': '6',
    '1e45375007c9edf827c83c1dafd1a78bd2fabecb': '经',
    'b7539565b06268d70a91cea2cd4178b4da798089': '王',
    '97817f695aacb359ffb5b8ca0717ca6344e84ccb': '应',
    'cc315ddd20b6361ef77cc82fbbc59f9ac40c3bd5': '专',
    '644caa33f64d9751aca184327eb27928b26775a7': '赵',
    'edc7496ac07d57b44a026de002422eec4f2ee1c4': '李',
    'cec031df25f4fc961f481e6029e9787fd0860d43': '以',
    'a07a8e4e1b273d55773605c33dbeb2b35ab0feff': '吴',
    '91106b5585628e13a9dd99c023436f0720204c33': '女',
    'dfe982c5707ac95c93c75705a38124fbd4e57446': '杨',
    '00acb9148038506dd725b383c8190a2db56ea763': '7',
    '79da38d1c5900b399df3f42a28217d404fe32620': '5',
    'f60ba3e0090eb10b4a1815e0c054fa44b7303aa0': '张',
    '651cc305ff99243489da82fbfecf020446d7c342': 'B',
    'd5f3892cd55e9f22947ac2aba291329711533e81': '本',
    '8410c547e1dd21cd175d0f0f9ae84bfd30940ade': '男',
    '3267ee0dd0cb0e11617788ae753cc369a5c4baae': '博',
    'fd05decfb4e1794a224a9129f6ef92993d325a81': '3',
    '14b002b6241afb1b968cf0b812854d9b0a212cdf': '无',
    'f3686b516fafbdcca4eeef2648e0951f3889de32': '9',
    'a03d1be9168f50f083686d63411c82cbea6db391': '生',
    '4f20412aff68f7f19790761a1cbcaeaa7db0c9e9': '验',
    '7f129bc4cd21e1eb51c528932e43abb805db2d6c': '8',
    'a935b6d4b4c63c3c25314ed2e497570a697b88ff': '下',
    '0cb8891b4b93f0060b25a8a190b37ebf0fe4837e': '科',
    'c6cd476937866c3aa89dd73db226af18e9d4e3f4': '1',
    'f95ae3a1652a55f24f34d9c2f32eeac3f5230b2d': '4',
    '4083c6fe15c7f55624286691f09d18c8a54bc4f1': 'M',
    '9c22abfda3684ef55fb4d14c8abb2c8cc191cb74': '中',
    'a0d2037fded629d8ee3d3563c2974935e84f6e41': '硕',
    '40d32e734682aee7df1bacdae7db056019b7fdd6': '届',
    'a67d95e35ce49467e2b0ff549a173043460742d8': '2',
    '0889937589fdd669a172f4e65707938a3dc2242a': '刘',
    'f18e8a977aeb769874d0d8714c3153109658d1b5': '士',
    '1b25a4e145326143b528672986fea06f0549d180': '陈',
    '7604e45e05cf4b3a98804474c15f2c4096fa410b': '高',
    'cd5372f2cd6103cd7895a4ca1847860da14a7e59': '大',
    'c901ab9eb8a4d5539778a3a34f17f0515cb2ef64': '0',
    '4b498c37e97d53a91d68bda4cfd4848adc977f06': 'E',
    '3486580a1462d28776136bf1f620b3dec79c982b': '周',
    '1ac40770b08fa65fac385230e8d9799257b47380': 'A',
    '9a379807d2bf090c94f1a03cf3fd18c6282882c1': '校',
    '77880914931fb6dda97269a9156404745f609d35': '黄'
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

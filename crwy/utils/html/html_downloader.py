#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: wuyue92tree@163.com

import requests


class HtmlDownloader(object):
    """ 下载器 """
    def __init__(self):
        self.session = requests.session()

    def download(self, url, method='GET', timeout=60, **kwargs):
        """
        请求页面
        :param url: 目标地址
        :param method: 请求方式
        :param timeout: 初始化超市时间
        :param kwargs: 更多requests参数
        :return: 返回requests session对象
        """
        if method == 'GET':
            return self.session.get(url, timeout=timeout, **kwargs)
        else:
            return self.session.post(url, timeout=timeout, **kwargs)

    def downloadFile(self, url, save_path='./data/'):
        """
        请求文件
        :param url: 目标地址
        :param save_path: 保存路径
        :return: 返回保存路径
        """
        file_name = url.split('/')[-1]
        file = self.download(url, stream=True)
        with open(save_path+file_name, 'wb') as f:
            for chunk in file.iter_content(chunk_size=1024):
                if chunk:  # filter out keep-alive new chunks
                    f.write(chunk)
                    f.flush()
            f.close()
        return save_path+file_name

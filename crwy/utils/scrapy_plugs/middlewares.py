#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: wuyue
@contact: wuyue92tree@163.com
@software: PyCharm
@file: middlewares.py
@create at: 2018-06-26 18:21

这一行开始写关于本文件的说明与解释

通过redis hash表记录站点cookie

key为 cookie_pool:SITE (SITE需要在settings中指定)
field为 账号cookie的唯一标识，可以是username，id等，具体自行约定
value为 cookie值，必须为json格式

"""
import datetime
import random
from scrapy.downloadermiddlewares.retry import RetryMiddleware
from scrapy.exceptions import IgnoreRequest
from scrapy_redis.connection import get_redis_from_settings

from crwy.utils.common import datetime2str
from crwy.utils.data.RedisHash import RedisHash
from crwy.exceptions import CrwyScrapyPlugsException, CrwyCookieValidException
from crwy.utils.scrapy_plugs.dupefilters import release_dupefilter_key


class CookieMiddleware(RetryMiddleware):
    """
    cookie_pool
        eg: '{"a": 1, "b": "aaa"}'
    """

    def __init__(self, settings):
        super(CookieMiddleware, self).__init__(settings)
        self.site = settings.get('SITE', None)
        if not self.site:
            raise CrwyScrapyPlugsException('SITE_NOT_SET')

        self.server = get_redis_from_settings(settings)

        self.h = RedisHash(
            'cookie_pool:{}'.format(self.site),
            server=self.server
        )

    def process_request(self, request, spider):
        """
        cookie_user不为空时，获取cookie_user对应的cookie
        keep_cookie_user为True时，将设置cookie_user，并传递到子请求
        :param request:
        :param spider:
        :return:
        """
        if request.meta.get('cookie_user', ''):
            user = request.meta.get('cookie_user')
        else:
            users = self.h.hkeys()
            if len(users) > 0:
                user = random.choice(users)
                if request.meta.get('keep_cookie_user', False) is True:
                    request.meta['cookie_user'] = user
            else:
                raise CrwyScrapyPlugsException(
                    'no user in cookie_pool:{}'.format(self.site))
        cookie = self.h.hget(user)
        if cookie:
            # 字典存入redis，取出时未string，通过eval进行还原
            request.cookies = eval(cookie)
            spider.logger.debug('get_cookie_success: {}'.format(
                user.decode('utf-8')))
        else:
            spider.logger.warning('get_cookie_failed: {}'.format(
                user.decode('utf-8')))


class LimitCookieMiddleware(CookieMiddleware):
    """
    在cookieMiddleware基础上限制账号

    1. 每日搜索上限
        通过 update_requests_count method 更新有效请求次数
    2. cookie失效标识
        捕捉 CrwyCookieValidException 异常更改标识状态
    """
    def __init__(self, settings):
        super(LimitCookieMiddleware, self).__init__(settings)

        # 每日搜索上限
        self.search_limit = RedisHash(
            'search_limit:{}'.format(self.site), server=self.server)
        # cookie失效标识， 1为cookie失效
        self.account_limit = RedisHash(
            'account_limit:{}'.format(self.site), server=self.server)

    def get_requests_count(self, request):
        user = request.meta.get('cookie_user')
        today = datetime2str(datetime.datetime.now(), fmt='%Y-%m-%d')
        if not self.search_limit.hget(user):
            count = 1
        else:
            date, count = self.search_limit.hget(
                user).decode('utf-8').split('|')
            if date == today:
                count = int(count)
            else:
                count = 1
        return user, count

    def update_requests_count(self, request, spider):
        """
        请求完毕后添加详情页计数
        :param request:
        :param spider:
        :return:
        """
        user, count = self.get_requests_count(request)
        today = datetime2str(datetime.datetime.now(), fmt='%Y-%m-%d')
        count += 1
        self.search_limit.hset(user, '{}|{}'.format(today, count))
        spider.logger.debug('update search_limit: {} {}'.format(
            user.decode('utf-8'), count))

    def _retry(self, request, reason, spider):
        callback = super(LimitCookieMiddleware, self)._retry(
            request, reason, spider
        )
        if not callback:
            if isinstance(reason, CrwyCookieValidException):
                user = request.meta.get('cookie_user')
                self.account_limit.hset(user, 1)
                spider.logger.warning('account limit: {} after retry'.format(
                    user.decode('utf-8')))
                raise IgnoreRequest
        else:
            return callback

    def process_request(self, request, spider):
        super(LimitCookieMiddleware, self).process_request(request, spider)

        user, count = self.get_requests_count(request)

        dupefilter_key = request.meta.get('dupefilter_key')

        # 判断account_limit, 若为1则表示账号禁用中
        if self.account_limit.hget(user) == b'1':
            spider.logger.warning(
                'account_limit: {}'.format(user.decode('utf-8')))
            release_dupefilter_key.call(spider, dupefilter_key)
            raise IgnoreRequest

        # 判断是否为受保护搜索账号
        if user.decode('utf-8') in spider.custom_settings.get(
                'SAFE_SEARCH_ACCOUNT'):
            if count >= spider.custom_settings.get('SAFE_SEARCH_LIMIT'):
                spider.logger.warning(
                    '{} safe_search_limit: {}'.format(
                        user.decode('utf-8'), count))
                release_dupefilter_key.call(spider, dupefilter_key)
                raise IgnoreRequest

        # 判断search_limit，若大于上限则跳过
        if count >= spider.custom_settings.get('SEARCH_LIMIT'):
            spider.logger.warning(
                '{} search_limit: {}'.format(user.decode('utf-8'), count))
            release_dupefilter_key.call(spider, dupefilter_key)
            raise IgnoreRequest

        if not request.cookies:
            spider.logger.warning('cookie is empty: {}'.format(
                user.decode('utf-8')))
            release_dupefilter_key.call(spider, dupefilter_key)
            raise IgnoreRequest

#! /usr/bin/env python
# -*- coding: utf-8 -*-
# Author: wuyue
# Email: wuyue92tree@163.com


from __future__ import print_function, unicode_literals

import email
import re
import traceback
import imaplib

from imapclient import IMAPClient
from email.header import decode_header

imaplib._MAXLINE = 10000000

SEEN = br'\Seen'


class MailReceiver(IMAPClient):
    def __init__(self, host, timeout=60, **kwargs):
        super(MailReceiver, self).__init__(host, timeout=timeout, **kwargs)

    def get_folder_list(self):
        """
        获取邮箱文件夹
        :return: list
        """
        folders = self.list_folders()
        res_list = []
        for folder in folders:
            if folder:
                # print(folder[2].encode("utf-8"))
                res_list.append(folder[2])
        return res_list

    def get_message_id_list(self, mailbox='INBOX', search_='all'):
        """
        获取邮件ID列表
        :param mailbox: 邮箱文件夹
        :param search_: 搜索规则
        :return: list
        """
        self.select_folder(mailbox)
        # message_list = self.server.search('ON 21-Dec-2017')
        message_list = self.search(search_)
        return message_list

    def get_message_list(self, message_id_list):
        """
        获取邮件列表
        :param message_id_list: 邮件ID列表
        :return: dict   id:email
        """
        message_list = self.fetch(
            message_id_list, ['INTERNALDATE', 'FLAGS', 'BODY.PEEK[]'])
        if not message_list:
            return

        return message_list

    @staticmethod
    def parse_email(m, flag=None):
        """
        解析邮件header内容
        :param m: 原内容
        :param flag: 解析类型标识
        :return: 编码转换后内容
        """
        try:
            res = []
            for s, c in decode_header(m):
                if c:
                    res.append(s.decode(c, 'ignore'))
                else:
                    res.append(s.decode('utf-8') if isinstance(s, bytes) else s)

            if not res:
                return

            # 处理邮件发送方 返回邮箱地址
            if flag == 'from':
                res = re.findall(
                    '[0-9a-zA-Z_\.]{0,19}@[0-9a-zA-Z\.]{1,100}', res[1])
                return res[0]

            # 处理邮件接收方 返回邮箱地址列表
            if flag == 'to':
                new_res = []
                for e in res[0].split(','):
                    em = re.findall('[0-9a-zA-Z_\.]{0,19}@[0-9a-zA-Z\.]{1,100}', e)
                    if em:
                        new_res.append(em[0])

                return new_res

            return res[0]
        except Exception as e:
            traceback.print_exc(e)
            return res

    def get_message_content(self, message):
        """
        获取邮件内容
        :param message:
        :return:
        """
        try:
            while True:
                res = {}
                msg = email.message_from_bytes(message[b'BODY[]'])
                res['subject'] = self.parse_email(msg['Subject'])
                res['from'] = self.parse_email(msg['From'], flag='from')
                res['to'] = self.parse_email(msg['To'], flag='to')
                res['date'] = self.parse_email(msg['Date'])

                for par in msg.walk():
                    if not par.is_multipart():
                        name = par.get_param("name")
                        if name:
                            # print(name)
                            pass
                        else:
                            body = par.get_payload(decode=True)
                            if not body:
                                continue
                            try:
                                code = par.get_content_charset()
                                res['body'] = body.decode(code, 'ignore')
                            except TypeError:
                                res['body'] = body
                return res

        except Exception as e:
            traceback.print_exc(e)
            return

    def delete_message(self, messages, deleted_folder="Deleted Messages"):
        """
        删除邮件
        :param messages:
        :param deleted_folder:
        :return:
        """
        try:
            self.add_flags(messages, SEEN)
            if deleted_folder:
                # 将邮件移动到 已删除
                self.copy(messages, deleted_folder)
            self.delete_messages(messages)
            self.expunge()
            return True
        except Exception as e:
            traceback.print_exc(e)
            return False

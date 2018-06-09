#! /usr/bin/env python
# -*- coding: utf-8 -*-
# Author: wuyue
# Email: wuyue92tree@163.com


from __future__ import print_function

import email
import traceback
import imaplib
from imapclient import IMAPClient
from email.header import decode_header
from retrying import retry


imaplib._MAXLINE = 10000000

SEEN = br'\Seen'


class MailReceiver(object):
    def __init__(self, host=None, username=None, password=None,
                 port=None, SSL=True):
        self.server = IMAPClient(host=host, ssl=SSL, timeout=100)
        self.username = username
        self.password = password

    @retry(stop_max_attempt_number=3)
    def folder_list(self):
        folders = self.server.list_folders()

        res_list = []
        for folder in folders:
            if folder:
                # print(folder[2].encode("utf-8"))
                res_list.append(folder[2].encode("utf-8"))
        return res_list

    @retry(stop_max_attempt_number=3)
    def message_list(self, mailbox='INBOX', search_='all'):
        self.server.select_folder(
            mailbox)
        # message_list = self.server.search('ON 21-Dec-2017')
        message_list = self.server.search(search_)
        return message_list

    @retry(stop_max_attempt_number=3)
    def download_message_list(self, message_list):
        msg_data = self.server.fetch(
            message_list, ['INTERNALDATE', 'FLAGS', 'BODY.PEEK[]'])
        if not msg_data:
            # print(self.username)
            return None, None
        return message_list, msg_data

    def get_content(self, message):
        try:
            while True:
                res = {}
                msg = email.message_from_string(message['BODY[]'])
                for s, c in decode_header(msg['subject']):
                    try:
                        res['subject'] = s.decode(c, 'ignore')
                    except TypeError:
                        res['subject'] = s
                        # print('Subject: ' + res['subject'])
                        # print('From: ' + email.utils.parseaddr(msg['from'])[1])
                        # print('To: ' + email.utils.parseaddr(msg['to'])[1])

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

                # print('____________________________________________')
                return res

        except Exception as e:
            traceback.print_exc()
            # print('got msg error: %s' % e)
            return

    def delete_message(self, messages, deleted_folder=u"Deleted Messages"):
        try:
            self.server.add_flags(messages, SEEN)
            if deleted_folder:
                # 将邮件移动到 已删除
                self.server.copy(messages, deleted_folder)
            self.server.delete_messages(messages)
            self.server.expunge()
            return True
        except Exception as e:
            # print("邮件删除失败： %s" % e)
            traceback.print_exc()
            return

    def close(self):
        self.server.logout()

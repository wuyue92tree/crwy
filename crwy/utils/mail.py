#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: wuyue92tree@163.com

import smtplib
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from configparser import NoSectionError

try:
    from crwy.cmdline import get_project_settings
except ImportError:
    pass

try:
    default = __import__(get_project_settings())
    MAIL_HOST = getattr(default.settings, 'MAIL_HOST', None)
    MAIL_USER = getattr(default.settings, 'MAIL_USER', None)
    MAIL_PASSWORD = getattr(default.settings, 'MAIL_PASSWORD', None)
    MAIL_POSTFIX = getattr(default.settings, 'MAIL_POSTFIX', None)
except NoSectionError:
    pass


class Mail(object):
    def __init__(self, mail_host=None, mail_user=None, mail_password=None, mail_postfix=None):
        if mail_host and mail_user and mail_password:
            self.mail_host, self.mail_user, self.mail_password, self.mail_postfix = mail_host, mail_user, mail_password, mail_postfix
        else:
            self.mail_host, self.mail_user, self.mail_password, self.mail_postfix = MAIL_HOST, MAIL_USER, MAIL_PASSWORD, MAIL_POSTFIX

    def send_mail(self, mail_to, sub, content, subtype='plain', charset='utf8',
                  enclosure=None, images=None):
        msg = MIMEMultipart()
        txt = MIMEText(content, _subtype=subtype, _charset=charset)
        msg.attach(txt)

        if enclosure:
            for path in enclosure:
                filename = path.split('/')[-1]
                att = MIMEText(open(path, 'rb').read(), 'base64', charset)
                att["Content-Type"] = 'application/octet-stream'
                att["Content-Disposition"] = 'attachment; filename="%s"' % filename
                msg.attach(att)

        if images:
            for path in images:
                imagename = path.split('/')[-1]
                image = MIMEImage(open(path, 'rb').read())
                image.add_header('Content-ID', '<%s>' % imagename)
                msg.attach(image)

        msg['Subject'] = sub
        msg['From'] = self.mail_user
        msg['To'] = ";".join(mail_to)

        try:
            server = smtplib.SMTP()
            server.connect(self.mail_host)
            server.login(self.mail_user, self.mail_password)
            server.sendmail(self.mail_user, mail_to, msg.as_string())
            server.close()
            return True
        except Exception, e:
            print str(e)
            return False

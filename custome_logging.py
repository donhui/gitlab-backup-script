#!/usr/bin/env python
#
# Copyright 2001-2002 by Vinay Sajip. All Rights Reserved.
#
# Permission to use, copy, modify, and distribute this software and its
# documentation for any purpose and without fee is hereby granted,
# provided that the above copyright notice appear in all copies and that
# both that copyright notice and this permission notice appear in
# supporting documentation, and that the name of Vinay Sajip
# not be used in advertising or publicity pertaining to distribution
# of the software without specific, written prior permission.
# VINAY SAJIP DISCLAIMS ALL WARRANTIES WITH REGARD TO THIS SOFTWARE, INCLUDING
# ALL IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL
# VINAY SAJIP BE LIABLE FOR ANY SPECIAL, INDIRECT OR CONSEQUENTIAL DAMAGES OR
# ANY DAMAGES WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER
# IN AN ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT
# OF OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.
#
# This file is part of the Python logging distribution. See
# http://www.red-dove.com/python_logging.html
#
"""Test harness for the logging module. Tests BufferingSMTPHandler, an alternative implementation
of SMTPHandler.

Copyright (C) 2001-2002 Vinay Sajip. All Rights Reserved.
"""
"""custome class BufferingSMTPHandler,add smtp auth feature.
Copyright (C) 2016 donghui. All Rights Reserved.
"""
import sys
import string
import logging
from logging.handlers import BufferingHandler
from logging import StreamHandler
from email.mime.text import MIMEText


class BufferingSMTPHandler(BufferingHandler):
    def __init__(self, mailhost, fromaddr, toaddrs, subject, username, password, capacity):
        logging.handlers.BufferingHandler.__init__(self, capacity)
        self.mailhost = mailhost
        self.mailport = None
        self.fromaddr = fromaddr
        self.toaddrs = toaddrs
        self.subject = subject
        self.username = username
        self.password = password
        self.setFormatter(logging.Formatter("%(asctime)s %(levelname)-5s %(message)s"))

    def flush(self):
        if len(self.buffer) > 0:
            try:
                import smtplib

                port = self.mailport
                if not port:
                    port = smtplib.SMTP_PORT
                smtp = smtplib.SMTP(self.mailhost, port)
                content = ""
                for record in self.buffer:
                    s = self.format(record)
                    print s
                    if "ERROR" in s.upper():
                        s = '<span style="color:red;">' + s + '</span>'
                    content = content + s + '<br/>'
                msg = MIMEText(content, 'html', 'utf-8')
                msg['Subject'] = self.subject
                msg['From'] = self.fromaddr
                msg['To'] = ','.join(self.toaddrs)
                msg["Accept-Charset"] = "ISO-8859-1,utf-8"
                smtp.login(self.username, self.password)
                smtp.sendmail(self.fromaddr, self.toaddrs, msg.as_string())
                smtp.quit()
            except:
                self.handleError(None)  # no particular record
            self.buffer = []


class ConsoleHandler(StreamHandler):
    def __init__(self):
        StreamHandler.__init__(self, stream=sys.stdout)
        self.setFormatter(logging.Formatter("%(asctime)s %(levelname)-5s %(message)s"))

if __name__ == "__main__":
    print "BufferingSMTPHandler"
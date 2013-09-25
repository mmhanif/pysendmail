#!/usr/bin/env python
# encoding: utf-8
"""
email.py

Created by Mahmood Hanif on 2012-11-05.
Copyright (c) 2012 Teknifi. All rights reserved.

Adapted from http://docs.python.org/2/library/email-examples.html
"""

import os
import smtplib
# For guessing MIME type based on file name extension
import mimetypes

from email import encoders
from email.message import Message
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

COMMASPACE = ', '


def sendmail(sender, recipients, subject, body, pathsToAttachments, cc_recipients=None, hostname='localhost', port=None, username=None, password=None, useTLS=False, useSSL=False, output=None):
    # Create body of message with attachments
    composed = _create_msg(sender, recipients, cc_recipients, subject, body, pathsToAttachments)
    
    # Now send or store the message
    if output:
        fp = open(output, 'w')
        fp.write(composed)
        fp.close()
    else:
        _send_mail(sender, recipients, cc_recipients, composed, hostname, port=port, username=username, password=password, useTLS=useTLS, useSSL=useSSL)



def _create_attachment(path):
    # Guess the content type based on the file's extension.  Encoding
    # will be ignored, although we should check for simple things like
    # gzip'd or compressed files.
    ctype, encoding = mimetypes.guess_type(path)
    if ctype is None or encoding is not None:
        # No guess could be made, or the file is encoded (compressed), so
        # use a generic bag-of-bits type.
        ctype = 'application/octet-stream'
    maintype, subtype = ctype.split('/', 1)
    if maintype == 'text':
        fp = open(path)
        # Note: we should handle calculating the charset
        msg = MIMEText(fp.read(), _subtype=subtype)
        fp.close()
    elif maintype == 'image':
        fp = open(path, 'rb')
        msg = MIMEImage(fp.read(), _subtype=subtype)
        fp.close()
    elif maintype == 'audio':
        fp = open(path, 'rb')
        msg = MIMEAudio(fp.read(), _subtype=subtype)
        fp.close()
    else:
        fp = open(path, 'rb')
        msg = MIMEBase(maintype, subtype)
        msg.set_payload(fp.read())
        fp.close()
        # Encode the payload using Base64
        encoders.encode_base64(msg)
    # Set the filename parameter
    filename = os.path.basename(path)
    msg.add_header('Content-Disposition', 'attachment', filename=filename)
    return msg
    
def _create_msg(sender, recipients, cc_recipients, subject, body, paths):
    # Create the enclosing (outer) message
    outer = MIMEMultipart()
    outer['Subject'] = subject
    outer['To'] = COMMASPACE.join(recipients)
    outer['From'] = sender
    if cc_recipients:
        outer['Cc'] = COMMASPACE.join(cc_recipients)

    for path in paths:
        if not os.path.isfile(path):
            continue
        msg = _create_attachment(path)
        outer.attach(msg)

    mainMsg = MIMEText('text', "plain")
    mainMsg.set_payload(body)
    outer.attach(mainMsg)
    
    return outer.as_string()

def _send_mail(sender, recipients, cc_recipients, msgString, hostname, port=None, username=None, password=None, useTLS= False, useSSL=False):
    connType = smtplib.SMTP_SSL if useSSL else smtplib.SMTP
    conn = connType(hostname, port) if port else connType(hostname)
    conn.set_debuglevel(False)
    if useTLS:
        conn.ehlo()        
        conn.starttls()
        conn.ehlo()
    if username and password:
        conn.login(username, password)
    try:
        all_recipients = recipients + cc_recipients if cc_recipients else recipients
        conn.sendmail(sender, all_recipients, msgString)
    finally:
        conn.close()


"""
email.py

Created by Mahmood Hanif

Adapted from http://docs.python.org/2/library/email-examples.html
"""

import os
import smtplib
import ssl
import mimetypes  # For guessing MIME type based on file name extension
from email import encoders
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

COMMASPACE = ', '


def sendmail(sender, recipients, subject, body, paths_to_attachments, cc_recipients=None,
             hostname='localhost', port=None, username=None, password=None,
             use_tls=False, use_ssl=False, output=None):
    # Create body of message with attachments
    composed = _create_msg(sender, recipients, cc_recipients, subject, body, paths_to_attachments)
    
    # Now send or store the message
    if output:
        fp = open(output, 'w')
        fp.write(composed)
        fp.close()
    else:
        _send_mail(sender, recipients, cc_recipients, composed,
                   hostname, port=port, username=username, password=password,
                   use_tls=use_tls, use_ssl=use_ssl)


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

    main_msg = MIMEText('text', "plain")
    main_msg.set_payload(body)
    outer.attach(main_msg)
    
    return outer.as_string()


def _send_mail(sender, recipients, cc_recipients, msg_string,
               hostname, port=None, username=None, password=None,
               use_tls=False, use_ssl=False):
    conn_type = smtplib.SMTP_SSL if (use_ssl and not use_tls) else smtplib.SMTP
    conn = conn_type(hostname, port) if port else conn_type(hostname)
    conn.set_debuglevel(False)
    if use_tls:
        context = ssl.SSLContext(ssl.PROTOCOL_TLS) if use_ssl else None
        conn.ehlo()
        conn.starttls(context=context)
        conn.ehlo()
    if username and password:
        conn.login(username, password)
    try:
        all_recipients = recipients + cc_recipients if cc_recipients else recipients
        conn.sendmail(sender, all_recipients, msg_string)
    finally:
        conn.close()


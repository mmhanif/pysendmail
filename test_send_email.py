"""
test_send_email.py

Created by Mahmood Hanif
"""

from send_email import sendmail


def test_local_output(sender):
    recipients = ["pysendmail.recipient@mailinator.com"]
    reply_to = sender
    cc_recipients = ["pysendmail.cced@mailinator.com"]
    subject = "test_local_output"
    paths = ['./send_email.py', './README.md']
    body = "This is a test"
    sendmail(sender, recipients, subject, body, paths, reply_to, cc_recipients, output='./test_local_output.txt')


def test_yahoo(sender, pwd):
    recipients = ["pysendmail.recipient@mailinator.com"]
    reply_to = sender
    cc_recipients = ["pysendmail.cced@mailinator.com"]
    subject = "test_yahoo"
    paths = ['./send_email.py', './README.md']
    body = "This is a test"
    hostname = "smtp.mail.yahoo.com"
    port = 25
    sendmail(sender, recipients, subject, body, paths, reply_to, cc_recipients,
             hostname=hostname, port=port, username=sender, password=pwd, use_tls=False, use_ssl=False)


def test_yahoo_plus(sender, pwd):
    recipients = ["pysendmail.recipient@mailinator.com"]
    reply_to = sender
    cc_recipients = ["pysendmail.cced@mailinator.com"]
    subject = "test_yahoo_plus"
    paths = ['./send_email.py', './README.md']
    body = "This is a test"
    hostname = "plus.smtp.mail.yahoo.com"
    port = 465
    sendmail(sender, recipients, subject, body, paths, reply_to, cc_recipients,
             hostname=hostname, port=port, username=sender, password=pwd, use_tls=False, use_ssl=True)


def test_gmail(sender, pwd):
    recipients = ["pysendmail.recipient@mailinator.com"]
    reply_to = sender
    cc_recipients = ["pysendmail.cced@mailinator.com"]
    subject = "test_gmail"
    paths = ['./send_email.py', './README.md']
    body = "This is a test"
    hostname = "smtp.gmail.com"
    port = 587
    sendmail(sender, recipients, subject, body, paths, reply_to, cc_recipients,
             hostname=hostname, port=port, username=sender, password=pwd, use_tls=True, use_ssl=True)


def test(sender, pwd):
    print("Testing local output")
    test_local_output(sender)
    # print("Testing Yahoo!")
    # test_yahoo(sender, pwd)
    # print("Testing Yahoo! Plus")
    # test_yahoo_plus(sender, pwd)
    # print("Testing Gmail")
    # test_gmail(sender, pwd)


def main():
    import sys
    sender = sys.argv[1]
    pwd = sys.argv[2]
    test(sender, pwd)


if __name__ == '__main__':
    main()


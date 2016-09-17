#! /usr/bin/python
# -*- encoding: utf-8 -*-
import smtplib, cgi

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from . import app

def send(me, you, subject, link_name, link):
    # me == my email address
    # you == recipient's email address

    # Create message container - the correct MIME type is multipart/alternative.
    msg = MIMEMultipart('alternative')
    msg['Subject'] = subject
    msg['From'] = me
    msg['To'] = you

    # Create the body of the message (a plain-text and an HTML version).
    text = "您好!\n您的{}链接为:\n{}".format(link_name, link)
    html = """\
    <html>
      <head></head>
      <body>
        <p>您好!<br>
           您的{}链接为:<a href="{}">{}</a>
        </p>
      </body>
    </html>
    """.format(cgi.escape(link_name), cgi.escape(link), cgi.escape(link))

    # Record the MIME types of both parts - text/plain and text/html.
    part1 = MIMEText(text, 'plain')
    part2 = MIMEText(html, 'html')

    # Attach parts into message container.
    # According to RFC 2046, the last part of a multipart message, in this case
    # the HTML message, is best and preferred.
    msg.attach(part1)
    msg.attach(part2)

    # Send the message via local SMTP server.
    s = smtplib.SMTP(app.config['SMTP_SERVER'])
    # sendmail function takes 3 arguments: sender's address, recipient's address
    # and message to send - here it is sent as one string.
    s.sendmail(me, you, msg.as_string())
    s.quit()

if __name__ == '__main__':
    send('no-reply@groups.thu-skyworks.org', 'zz593141477@gmail.com', '天空工场账号服务', '密码重置', 'https://thu-skyworks.org/')

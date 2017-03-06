#!/home/imyin/python_env/newspaper_python3/bin python3
# -*- coding: utf-8 -*-

"""
Created on 3/3/17 3:28 PM

@author: imyin

@File: send_mail
"""

import smtplib
import sys
from email.header import Header
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import Constants as cons

today_date = sys.argv[1]
current_time = sys.argv[2]


def get_contents():
    connection = cons.conn_mysql()
    try:
        with connection.cursor() as cursor:
            sql = (cons.select_news_mail.format(cons.news_table_name, today_date, current_time))
            x = cursor.execute(sql)
            result = cursor.fetchmany(x)
            # Collect the contents of article.
            return {item[u'title']: item[u'content'] for item in result}
    finally:
        connection.close()


def run_send():
    dict_contents = get_contents()
    msg = MIMEMultipart()
    msg[u'Subject'] = Header(u"Now,there are {} news to read.".format(len(dict_contents)))
    news = get_contents()
    if len(news) > 0:
        for k, v in news.items():
            mail_msg = u'<b>{}</b><br><p>{}</p>'.format(k, v)
            msg.attach(MIMEText(mail_msg, u'html', u'utf-8'))
    else:
        mail_msg = u"There is no news to read before 30 minutes."
        msg.attach(MIMEText(mail_msg, u'plain', u'utf-8'))

    to_addr = cons.TO_ADDR
    from_addr = cons.FROM_ADDR
    password = cons.PASSWORD
    # Send the email via our own SMTP server.
    s = smtplib.SMTP(cons.SMTP_SERVER, 25)
    s.login(from_addr, password)  # to login SMTP server.
    s.sendmail(from_addr, to_addr, msg.as_string())
    s.quit()

if current_time != u"23:20":
    run_send()

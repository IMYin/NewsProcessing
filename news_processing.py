#!/home/imyin/python_env/newspaper_python3/bin python3
# -*- coding: utf-8 -*-

"""
Created on 3/2/17 3:32 PM

@author: imyin

@File: news_processing
"""
import datetime
import time

import newspaper

import Constants as cons

current_time = (datetime.datetime.now()).strftime(u'%H:%M')


def get_article(url):
    article = newspaper.Article(url, language=u'zh')
    try:
        article.download()
        article.parse()
    except Exception as e:
        print(u"Something go wrong...Cannot download it...")
        pass
    article_title = article.title
    article_text = article.text
    # if len(article_title) == 0:
    #     article_title = article.meta_description
    return article_title, article_text


def get_content(time_now, retry=3):
    contents = {}
    try:
        builder = newspaper.build(cons.NEWS_RESOURCE, language=u'zh')
        news_size = builder.size()
        if news_size > 0:
            if time_now != u"08:20":
                for item in builder.articles:
                    for _ in range(retry):
                        time.sleep(0.001)
                        article_title, article_text = get_article(item.url)
                        if len(article_text) != 0 and len(article_title) != 0:
                            break
                    print(u"{} {} : {}-----{}".format(cons.today_str_Ymd, time_now, article_title, article_text))
                    contents[article_title] = article_text
                print(u"There are {} news...".format(news_size))
                print(u"-" * 100)
                return contents
        else:
            print(u"There is nothing to get...")
            return contents
    except Exception as e:
        print(u"Something go wrong...")
        pass


def insert_to_mysql(lines, collect_time):
    connection = cons.conn_mysql()
    try:
        with connection.cursor() as cursor:
            for k, v in lines.items():
                sql = cons.insert_news.format(cons.news_table_name)
                cursor.execute(sql, (cons.today_str_Ymd, collect_time, k, v))
            connection.commit()
    finally:
        connection.close()


# while True:
current_time = (datetime.datetime.now()).strftime(u'%H:%M')
if current_time != u"23:50":
    contents = get_content(current_time, retry=5)
    if len(contents) > 0:
        insert_to_mysql(contents, current_time)
        # time.sleep(1800)
        # else:
        #     break

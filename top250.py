# -*- coding:utf-8 -*-

import requests
from lxml import html
import MySQLdb
import time


def getTop250(cursor, db, start=0):
    payload = {'start': start, 'filter': ''}
    start_url = 'https://movie.douban.com/top250'
    headers={
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
        'Host':'movie.douban.com',
        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Encoding':'gzip, deflate, sdch, br',
        'Connection':'keep-alive'
    }
    response = requests.get(start_url,headers = headers, params=payload)
    # print response.text
    res = html.fromstring(response.text)
    li = res.xpath('//ol[@class="grid_view"]/li')
    for i in li:
        try:
            title = "".join(i.xpath('string(./div[@class="item"]/div[@class="info"]/div[@class="hd"]/a)').split())
        except:
            title = None
        try:
            content = "".join(i.xpath('./div[@class="item"]/div[@class="info"]/div[@class="bd"]/p/text()'))
        except:
            content = None
        try:
            star = i.xpath('./div[@class="item"]/div[@class="info"]/div[@class="bd"]/div[@class="star"]/span[@class="rating_num"]/text()')[0]
        except:
            star = None
        try:
            count = i.xpath('./div[@class="item"]/div[@class="info"]/div[@class="bd"]/div[@class="star"]/span[@class="rating_num"]/text()')[0]
        except:
            count = None
        try:
            quote = i.xpath('./div[@class="item"]/div[@class="info"]/div[@class="bd"]/p[@class="quote"]/span[@class="inq"]/text()')[0]
        except:
            quote = None
        # print title,content,star,count,quote
        # SQL 插入语句
        sql = '''INSERT INTO top250(title, content, star, count, quote) VALUES ("%s", "%s", "%s", "%s","%s")'''%(title, content, star, count, quote)
        try:
            # 执行sql语句
            cursor.execute(sql)
            # 提交到数据库执行
            db.commit()
            print title + 'commit'
        except Exception, e:
            # Rollback in case there is any error
            db.rollback()
            print e


if __name__ == '__main__':
    # 打开数据库连接
    db = MySQLdb.connect(host="localhost", user="root", passwd="123456", db="doubanmovie", charset='utf8')
    # 使用cursor()方法获取操作游标
    cursor = db.cursor()
    for i in range(0,25):
        getTop250(cursor, db, i*25)
        # 暂停10s
        time.sleep(10)
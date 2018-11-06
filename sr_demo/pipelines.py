# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.conf import settings
import pymysql
import pymysql.cursors
from twisted.enterprise import adbapi

class SrDemoPipeline(object):
    def __init__(self):
        config={
            "host": settings['MYSQL_HOST'],
            "user": settings['MYSQL_USER'],
            "password": settings['MYSQL_PASS'],
            "database": settings['MYSQL_DB']
        }
        # 指定数据库模块名和数据库参数
        self.dbpool = adbapi.ConnectionPool("pymysql",**config)

    # 使用twisted将mysql插入变成异步执行
    def process_item(self, item, spider):
        query = self.dbpool.runInteraction(self.do_insert, item)
        # 处理异常
        query.addErrback(self.handle_error, item, spider)

    # 处理异步插入的异常
    def handle_error(self, failure, item, spider):
        print(failure)

    # 执行插入
    def do_insert(self, cursor, item):
        url = item['url']
        title = item['title']
        print("url: ",url)
        print("title: ",title)

        try:
            sql = "INSERT INTO news(url,title) VALUES(%s,%s)"
            values = (url,title)
            cursor.execute(sql, values)
            return item
        except Exception as err:
            pass
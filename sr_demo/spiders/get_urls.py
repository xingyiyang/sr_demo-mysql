# -*- coding: utf-8 -*-

import scrapy
import redis

class GeturlsSpider(scrapy.Spider):
    name = 'get_urls'
    allowed_domains = ['news.stcn.com/']
    start_urls = ['http://news.stcn.com/']

    def parse(self, response):
        res = response.xpath('//ul[@class="news_list"]/li')
        r = redis.Redis(host='localhost', port=6379)
        for eh in res:
            r.lpush('read_urls:start_urls', eh.xpath('./p[@class="tit"]/a/@href').extract_first())

# -*- coding: utf-8 -*-

from scrapy_redis.spiders import RedisSpider
from sr_demo.items import UrlItem


class ReadUrlsSpider(RedisSpider):
    name = 'read_urls'
    redis_key = 'read_urls:start_urls'

    def parse(self, response):
        url = response.url
        title = response.xpath('//div[@class="intal_tit"]/h2/text()').extract_first()
        item = UrlItem()
        item['url'] = url
        item['title']= title
        yield item

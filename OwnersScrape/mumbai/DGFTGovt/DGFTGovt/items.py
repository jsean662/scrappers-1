# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class DgftgovtItem(scrapy.Item):
    name = scrapy.Field()
    email = scrapy.Field()
    mobile_no = scrapy.Field()
    address = scrapy.Field()
    index_no = scrapy.Field()
    type = scrapy.Field()
    valid_date = scrapy.Field()
    certification_no = scrapy.Field()

# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class MakaanItem(scrapy.Item):
    city = scrapy.Field()
    lowest_price = scrapy.Field()
    middle_price = scrapy.Field()
    highest_price = scrapy.Field()
    locality = scrapy.Field()
    txn_type = scrapy.Field()
    scraped_time = scrapy.Field()

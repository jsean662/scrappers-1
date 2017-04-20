# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class Acres99Item(scrapy.Item):
    society_name = scrapy.Field()
    locality_name = scrapy.Field()
    lower_price = scrapy.Field()
    upper_price = scrapy.Field()
    city = scrapy.Field()
    platform = scrapy.Field()
    date = scrapy.Field()


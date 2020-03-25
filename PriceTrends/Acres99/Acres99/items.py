# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class Acres99Item(scrapy.Item):
    city = scrapy.Field()
    rent_lowest_price = scrapy.Field()
    sale_lowest_price = scrapy.Field()
    rent_highest_price = scrapy.Field()
    sale_highest_price = scrapy.Field()
    locality = scrapy.Field()
    scraped_time = scrapy.Field()

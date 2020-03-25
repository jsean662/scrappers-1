# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class SteeltradersItem(scrapy.Item):
    Name = scrapy.Field()
    Address = scrapy.Field()
    Phone_No = scrapy.Field()
    platform = scrapy.Field()
    scraped_time = scrapy.Field()

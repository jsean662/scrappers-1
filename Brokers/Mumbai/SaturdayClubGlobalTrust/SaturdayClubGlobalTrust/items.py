# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class SaturdayclubglobaltrustItem(scrapy.Item):
    Name = scrapy.Field()
    Email_Address = scrapy.Field()
    Mobile_No = scrapy.Field()
    City = scrapy.Field()
    scraped_time = scrapy.Field()
    platform = scrapy.Field()

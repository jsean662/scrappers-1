# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class HudkuItem(scrapy.Item):
    Name = scrapy.Field()
    Address = scrapy.Field()
    Contact_No = scrapy.Field()
    Email_Id = scrapy.Field()
    Website = scrapy.Field()
    Fax_No = scrapy.Field()
    scraped_time = scrapy.Field()
    platform = scrapy.Field()
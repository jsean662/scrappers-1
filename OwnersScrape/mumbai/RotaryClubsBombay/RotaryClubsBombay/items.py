# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class RotaryclubsbombayItem(scrapy.Item):
    Member_Name = scrapy.Field()
    Club_Name = scrapy.Field()
    Mobile_No = scrapy.Field()
    Email_Id = scrapy.Field()
    platform = scrapy.Field()
    scraped_time = scrapy.Field()

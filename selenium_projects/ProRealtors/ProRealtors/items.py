# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ProrealtorsItem(scrapy.Item):
    Building_Name = scrapy.Field()
    CS_Info = scrapy.Field()
    Location = scrapy.Field()
    platform = scrapy.Field()
    scraped_time = scrapy.Field()

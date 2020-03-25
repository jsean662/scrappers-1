# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ZricksItem(scrapy.Item):
    company_name = scrapy.Field()
    email_id = scrapy.Field()
    platform = scrapy.Field()
    scraped_time = scrapy.Field()
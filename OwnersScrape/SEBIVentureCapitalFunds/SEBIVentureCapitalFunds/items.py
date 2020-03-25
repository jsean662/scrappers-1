# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class SebiventurecapitalfundsItem(scrapy.Item):
    name = scrapy.Field()
    email_id = scrapy.Field()
    contact_person = scrapy.Field()
    address = scrapy.Field()
    platform = scrapy.Field()
    scraped_time = scrapy.Field()

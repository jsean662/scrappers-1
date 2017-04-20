# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class AnandpropertiesagentsItem(scrapy.Item):
    company_name = scrapy.Field()
    broker_name = scrapy.Field()
    mobile_no = scrapy.Field()
    phone_no = scrapy.Field()
    address = scrapy.Field()
    data_id = scrapy.Field()
    description = scrapy.Field()
# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class SmartrealtorsItem(scrapy.Item):
    broker_name = scrapy.Field()
    mobile_no = scrapy.Field()
    phone_no = scrapy.Field()
    localities = scrapy.Field()
    city = scrapy.Field()
    platform = scrapy.Field()
    txn_type = scrapy.Field()
    property_type = scrapy.Field()
    email_id = scrapy.Field()
    second_email = scrapy.Field()
    data_id = scrapy.Field()
    company_name = scrapy.Field()
    description = scrapy.Field()
    second_name = scrapy.Field()
    website = scrapy.Field()
    scraped_time = scrapy.Field()

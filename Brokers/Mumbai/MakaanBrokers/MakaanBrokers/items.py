# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class MakaanbrokersItem(scrapy.Item):
    data_id = scrapy.Field()
    broker_name = scrapy.Field()
    localities = scrapy.Field()
    total_properties = scrapy.Field()
    buy_properties = scrapy.Field()
    rent_properties = scrapy.Field()
    property_type = scrapy.Field()
    agent_type = scrapy.Field()
    mobile_no = scrapy.Field()
    broker_rating = scrapy.Field()
    platfrom = scrapy.Field()
    scraped_time = scrapy.Field()
    city = scrapy.Field()
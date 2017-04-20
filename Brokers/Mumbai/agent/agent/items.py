# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class AgentItem(scrapy.Item):
    company = scrapy.Field()
    agent_name = scrapy.Field()
    phone = scrapy.Field()
    detail = scrapy.Field()
    platform = scrapy.Field()
    listing_date = scrapy.Field()

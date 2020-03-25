# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class BohrabusinessItem(scrapy.Item):
    category = scrapy.Field()
    name = scrapy.Field()
    contact_no = scrapy.Field()
    email_id = scrapy.Field()
    address = scrapy.Field()
    website = scrapy.Field()
    scraped_time = scrapy.Field()
# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class HindustanyellowpagesItem(scrapy.Item):
    name = scrapy.Field()
    mobile_no = scrapy.Field()
    phone_no = scrapy.Field()
    email_id = scrapy.Field()
    address = scrapy.Field()
    scraped_time = scrapy.Field()
    platform = scrapy.Field()
    website = scrapy.Field()


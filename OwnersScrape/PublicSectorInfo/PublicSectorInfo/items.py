# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class PublicsectorinfoItem(scrapy.Item):
    name = scrapy.Field()
    position = scrapy.Field()
    organisation = scrapy.Field()
    dob = scrapy.Field()
    telephone_no = scrapy.Field()
    mobile_no = scrapy.Field()
    email_address = scrapy.Field()
    # files = scrapy.Field()
    # file_urls = scrapy.Field()
    # file_path = scrapy.Field()
    scraped_time = scrapy.Field()
    platform = scrapy.Field()
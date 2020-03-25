# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class HousingownersItem(scrapy.Item):
    owner_name = scrapy.Field()
    owner_no = scrapy.Field()
    # config = scrapy.Field()
    # locality = scrapy.Field()

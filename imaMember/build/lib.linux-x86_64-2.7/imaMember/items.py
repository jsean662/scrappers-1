# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ImamemberItem(scrapy.Item):
    # define the fields for your item here like:
    a_name = scrapy.Field()
    branch = scrapy.Field()
    postalcode = scrapy.Field()
    pass

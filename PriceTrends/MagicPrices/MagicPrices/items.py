# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class MagicpricesItem(scrapy.Item):
    area_name = scrapy.Field()
    sale_price_range = scrapy.Field()
    sale_avg_price = scrapy.Field()
    rent_price_range = scrapy.Field()
    rent_avg_price = scrapy.Field()
    property_type = scrapy.Field()
    city = scrapy.Field()
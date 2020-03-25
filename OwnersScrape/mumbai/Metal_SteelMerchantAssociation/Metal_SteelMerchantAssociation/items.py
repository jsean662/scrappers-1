# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class MetalSteelmerchantassociationItem(scrapy.Item):
    Name = scrapy.Field()
    Company_Name = scrapy.Field()
    Contact_No = scrapy.Field()
    Platform = scrapy.Field()
    scraped_time = scrapy.Field()

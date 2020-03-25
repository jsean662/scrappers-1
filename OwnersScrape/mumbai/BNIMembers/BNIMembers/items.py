# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class BnimembersItem(scrapy.Item):
    Chapter_Name = scrapy.Field()
    Chapter_Address = scrapy.Field()
    Member_Name = scrapy.Field()
    Contact_no = scrapy.Field()
    Phone_no = scrapy.Field()
    Website = scrapy.Field()
    Member_Address = scrapy.Field()
    Member_Company = scrapy.Field()
    Member_Proffesion = scrapy.Field()
    scraped_time = scrapy.Field()
    platform = scrapy.Field()

# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class DiasupplyDirectoryItem(scrapy.Item):
    company_name = scrapy.Field()
    contact_no = scrapy.Field()
    contact_person = scrapy.Field()
    website = scrapy.Field()
    office_no = scrapy.Field()
    QBC_no = scrapy.Field()
    email_ids = scrapy.Field()
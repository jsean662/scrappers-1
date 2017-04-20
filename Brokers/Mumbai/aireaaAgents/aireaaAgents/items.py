# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Item, Field


class AireaaagentsItem(Item):
    data_id = Field()
    contact_person = Field()
    company_name = Field()
    mobile_no = Field()
    phone_no = Field()
    email_id = Field()
    address = Field()
    locality = Field()
    city = Field()
    platform = Field()
    scraped_time = Field()
    add_lat = Field()
    add_longt = Field()
    sublocality = Field()
    website = Field()


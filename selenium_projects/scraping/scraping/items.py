# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ScrapingItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    #'locality':'','sub_loc':'','sqft':'','rent_price':'','title':'','detail':'','bed':'','flr':'','t_flr':'','depo':'','status':'','email':''
    locality = scrapy.Field()
    sub_loc = scrapy.Field()
    sqft = scrapy.Field()
    rent_price = scrapy.Field()
    title = scrapy.Field()
    detail = scrapy.Field()
    bed = scrapy.Field()
    bath = scrapy.Field()
    flr = scrapy.Field()
    t_flr = scrapy.Field()
    depo = scrapy.Field()
    status = scrapy.Field()
    
    pass

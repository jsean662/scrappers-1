# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class PropertywalaCommercialItem(scrapy.Item):
    carpet_area = scrapy.Field()
    updated_date = scrapy.Field()
    management_by_landlord = scrapy.Field()
    areacode = scrapy.Field()
    mobile_lister = scrapy.Field()
    google_place_id = scrapy.Field()
    age = scrapy.Field()
    address = scrapy.Field()
    price_on_req = scrapy.Field()
    sublocality = scrapy.Field()
    config_type = scrapy.Field()
    platform = scrapy.Field()
    city = scrapy.Field()
    listing_date = scrapy.Field()
    txn_type = scrapy.Field()
    property_type = scrapy.Field()
    Building_name = scrapy.Field()
    lat = scrapy.Field()
    longt = scrapy.Field()
    locality = scrapy.Field()
    Status = scrapy.Field()
    listing_by = scrapy.Field()
    name_lister = scrapy.Field()
    Selling_price = scrapy.Field()
    Monthly_Rent = scrapy.Field()
    Details = scrapy.Field()
    data_id = scrapy.Field()
    Possession = scrapy.Field()
    Launch_date = scrapy.Field()
    price_per_sqft = scrapy.Field()
    Bua_sqft = scrapy.Field()
    quality1 = scrapy.Field()
    quality2 = scrapy.Field()
    quality3 = scrapy.Field()
    quality4 = scrapy.Field()
    scraped_time = scrapy.Field()

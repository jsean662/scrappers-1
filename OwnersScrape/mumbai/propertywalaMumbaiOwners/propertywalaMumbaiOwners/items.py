# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class PropertywalamumbaiownersItem(scrapy.Item):
    image_urls = scrapy.Field()
    images = scrapy.Field()
    image_path = scrapy.Field()
    Status = scrapy.Field()
    price_per_sqft = scrapy.Field()
    areacode = scrapy.Field()
    mobile_lister = scrapy.Field()
    longt = scrapy.Field()
    config_type = scrapy.Field()
    Details = scrapy.Field()
    txn_type = scrapy.Field()
    property_type = scrapy.Field()
    Possession = scrapy.Field()
    city = scrapy.Field()
    management_by_landlord = scrapy.Field()
    locality = scrapy.Field()
    quality1 = scrapy.Field()
    quality2 = scrapy.Field()
    quality3 = scrapy.Field()
    quality4 = scrapy.Field()
    platform = scrapy.Field()
    Selling_price = scrapy.Field()
    Building_name = scrapy.Field()
    updated_date = scrapy.Field()
    Bua_sqft = scrapy.Field()
    name_lister = scrapy.Field()
    price_on_req = scrapy.Field()
    address = scrapy.Field()
    lat = scrapy.Field()
    Launch_date = scrapy.Field()
    google_place_id = scrapy.Field()
    listing_by = scrapy.Field()
    data_id = scrapy.Field()
    age = scrapy.Field()
    listing_date = scrapy.Field()
    carpet_area = scrapy.Field()
    sublocality = scrapy.Field()
    Monthly_Rent = scrapy.Field()
    scraped_time = scrapy.Field()

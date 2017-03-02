# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Item, Field


class MakaanKolkatarentItem(Item):
    carpet_area = Field()
    updated_date = Field()
    management_by_landlord = Field()
    areacode = Field()
    mobile_lister = Field()
    google_place_id = Field()
    age = Field()
    address = Field()
    price_on_req = Field()
    sublocality = Field()
    config_type = Field()
    platform = Field()
    city = Field()
    listing_date = Field()
    txn_type = Field()
    property_type = Field()
    Building_name = Field()
    lat = Field()
    longt = Field()
    locality = Field()
    Status = Field()
    listing_by = Field()
    name_lister = Field()
    Selling_price = Field()
    Monthly_Rent = Field()
    Details = Field()
    data_id = Field()
    Possession = Field()
    Launch_date = Field()
    price_per_sqft = Field()
    Bua_sqft = Field()
    quality1 = Field()
    quality2 = Field()
    quality3 = Field()
    quality4 = Field()
    scraped_time=Field()

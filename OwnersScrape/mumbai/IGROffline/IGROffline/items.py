# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class IgrofflineItem(scrapy.Item):
    Vilekhacha_Prakar = scrapy.Field()
    Mobadala = scrapy.Field()
    Bajarbhav = scrapy.Field()
    Bhumapan = scrapy.Field()
    Khetraphal = scrapy.Field()
    Akarani_Kinva = scrapy.Field()
    Dastevaj_Karun_Denarya = scrapy.Field()
    Dastevaj_Karun_Ghenarya = scrapy.Field()
    Dastevaj_Karun_Date = scrapy.Field()
    Dast_Nondani_Date = scrapy.Field()
    Anukramank = scrapy.Field()
    Bajarbhav_Mudrank = scrapy.Field()
    Bajarbhav_Nondani = scrapy.Field()
    town = scrapy.Field()
    page_no = scrapy.Field()


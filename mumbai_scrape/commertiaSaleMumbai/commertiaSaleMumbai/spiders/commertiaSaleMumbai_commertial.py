# -*- coding: utf-8 -*-
import scrapy


class CommertiasalemumbaiCommertialSpider(scrapy.Spider):
    name = "commertiaSaleMumbai_commertial"
    allowed_domains = ["commertia.in"]
    start_urls = [
        'http://www.commertia.in/search-property/Mumbai/SALE?propertyTypes=IT_ITES_OFFICE&propertyTypes=COMMERCIAL_OFFICE&propertyTypes=INDUSTRIAL_SHED&propertyTypes=INDUSTRIAL_LAND&propertyTypes=COMMERCIAL_LAND&propertyTypes=SHOWROOM&propertyTypes=INDUSTRIAL_WAREHOUSE/',
    ]

    def parse(self, response):
        pass

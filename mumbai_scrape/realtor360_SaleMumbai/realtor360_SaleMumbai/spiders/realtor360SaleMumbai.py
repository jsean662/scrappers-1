# -*- coding: utf-8 -*-
import scrapy


class Realtor360salemumbaiSpider(scrapy.Spider):
    name = "realtor360SaleMumbai"
    allowed_domains = ["360realtors.com"]
    start_urls = ['http://360realtors.com/']

    def parse(self, response):
        pass

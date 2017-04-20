# -*- coding: utf-8 -*-
import scrapy
from scrapy.selector import Selector
from ..items import LocalitiesItem


class LocalityspiderSpider(scrapy.Spider):
    name = "LocalitySpider"
    allowed_domains = ["https://www.commonfloor.com"]
    start_urls = [
        'https://www.commonfloor.com/kolkata-city',
        'https://www.commonfloor.com/mumbai-city',
        'https://www.commonfloor.com/hyderabad-city',
        'https://www.commonfloor.com/pune-city',
        'https://www.commonfloor.com/hyderabad-city',
        'https://www.commonfloor.com/delhi-city',
        'https://www.commonfloor.com/bangalore-city',
    ]

    def parse(self, response):
        records = Selector(response).xpath('//*[@id="localitysas"]/div[2]')

        item = LocalitiesItem()
        Locality = records.xpath('//*[@id="localitysas"]//*/li/div/a/text()').extract()
        for loc in Locality:
            item['Locality'] = loc
            item['City'] = response.url.split('.com/')[1].split('-')[0]
            item['Platform'] = 'CommonFloor'
            yield item

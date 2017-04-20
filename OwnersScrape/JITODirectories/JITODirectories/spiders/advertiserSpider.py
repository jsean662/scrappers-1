# -*- coding: utf-8 -*-
import scrapy
from scrapy.selector import Selector
from scrapy.http import Request
from ..items import JitodirectoriesItem


class AdvertiserspiderSpider(scrapy.Spider):
    name = "advertiserSpider"
    allowed_domains = ["http://jito.org/"]
    start_urls = [
        'http://jito.org/trade/search?advertiser=&locale=2&category=1&cmdSubmit.x=42&cmdSubmit.y=27/',
    ]

    def parse(self, response):
        records = Selector(response)

        item = JitodirectoriesItem()
        data = records.xpath('//*[@id="Innerpage_Container"]/div[1]/div[1]/div/div[2]/div[contains(@class,"media_blog ")]')

        for i in data:
            name = i.xpath('.//div[2]/h3/span/a/text()').extract_first(default='-')
            if name == '-':
                item['name'] = i.xpath('.//div[2]/h3/span/text()').extract_first(default='-')
            else:
                item['name'] = name

            item['contact_no'] = i.xpath('.//div[2]/div[2]/span[2]/text()').extract_first(default='-')

            item['email_id'] = i.xpath('.//div[2]/div[3]/span[2]/a/text()').extract_first(default='-')

            item['address'] = i.xpath('.//div[2]/div[4]/span[2]/text()').extract_first(default='-')

            yield item

        url = response.xpath('//*[@id="Innerpage_Container"]/div[1]/div[1]/div/div[2]/div[11]/ul/li[@class="next"]/a/@href').extract_first()
        yield Request(url, callback=self.parse, dont_filter=True)

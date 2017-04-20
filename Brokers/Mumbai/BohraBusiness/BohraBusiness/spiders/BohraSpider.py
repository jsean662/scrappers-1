# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request
from scrapy.selector import Selector
from ..items import BohrabusinessItem


class BohraspiderSpider(scrapy.Spider):
    name = "BohraSpider"
    allowed_domains = ["bohrabusiness.com"]
    start_urls = [
        'http://bohrabusiness.com/index.php/business-listing/',
    ]

    custom_settings = {
        'DOWNLOAD_DELAY': 3.0,
    }

    def parse(self, response):
        links = Selector(response).xpath('/*//div[@class="item-list"]//*/a/@href').extract()

        for link in links:
            url = 'http://bohrabusiness.com/' + link
            yield Request(url, callback=self.second_stage)

    def second_stage(self, response):
        records = Selector(response).xpath('//*[@id="block-bohrabusiness-content"]/div/div/div/div/table/tbody/tr')

        for r in records:
            txt = r.xpath('.//td[2]/p/span[@class="locality"]/text()').extract_first(default='None')
            if 'Mumbai' in txt:
                link = r.xpath('.//td[1]/a/@href').extract_first()
                if link is not None:
                    url = 'http://bohrabusiness.com/' + link
                    yield Request(url, callback=self.third_stage)

    def third_stage(self, response):
        record = Selector(response)

        item = BohrabusinessItem()
        item['name'] = record.xpath('//*[@id="block-bohrabusiness-page-title"]/div/h1/span/text()').extract_first()

        address = record.xpath('//*[@id="block-bohrabusiness-content"]/div/article/div/div[contains(@class,"address")]/div[2]/p/text()').extract()
        item['address'] = []
        if address is not None:
            for a in address:
                item['address'].append(a.strip())

        item['contact_no'] = record.xpath('//*[@id="block-bohrabusiness-content"]/div/article/div/div[contains(@class,"phone")]/div[2]/div/a/text()').extract_first()

        item['category'] = record.xpath('//*[@id="block-bohrabusiness-content"]/div/article/div/div[contains(@class,"category")]/div[2]/div/text()').extract_first()

        item['website'] = record.xpath('//*[@id="block-bohrabusiness-content"]/div/article/div/div[contains(@class,"website")]/div[2]/a/text()').extract_first()

        item['email_id'] = record.xpath('//*[@id="block-bohrabusiness-content"]/div/article/div/div[contains(@class,"email")]/div[2]/a/text()').extract_first()

        yield item

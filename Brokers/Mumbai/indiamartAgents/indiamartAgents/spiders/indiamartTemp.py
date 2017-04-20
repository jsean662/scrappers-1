# -*- coding: utf-8 -*-
import scrapy
from scrapy.selector import Selector
from ..items import IndiamartagentsItem
from datetime import datetime


class IndiamarttempSpider(scrapy.Spider):
    name = "indiamartTemp"
    allowed_domains = []
    start_urls = [
        'file:///C:/Users/Vic/Downloads/Real%20Estate%20Agent%20in%20Mumbai.html',
    ]

    def parse(self, response):

        item = IndiamartagentsItem()
        page = Selector(response)

        agents = page.xpath('//div[contains(@class,"wlm  city ")]/div[contains(@id,"LST")]')

        for agent in agents:
            item['scraped_time'] = datetime.now().strftime('%m/%d/%Y')
            item['city'] = 'Mumbai'

            item['description'] = agent.xpath('.//p[contains(@id,"trimmed_desc")]/text()').extract()

            item['company_name'] = agent.xpath('./*//a[@class="lcname"]/text()').extract_first()

            item['phone_no'] = agent.xpath('.//span[contains(@id,"pns")]/text()').extract_first()

            item['locality'] = agent.xpath('.//div[@class="nes"]/span[@class="clg"]/text()').extract_first().strip()

            yield item

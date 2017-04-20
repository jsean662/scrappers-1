# -*- coding: utf-8 -*-
import scrapy
from scrapy.selector import Selector
from ..items import SebiventurecapitalfundsItem
from datetime import datetime


class StartupindiafundsspiderSpider(scrapy.Spider):
    name = "StartupIndiaFundsSpider"
    allowed_domains = ["startupindia.gov.in"]
    start_urls = [
        'http://www.startupindia.gov.in/funds.php',
    ]

    def parse(self, response):
        record = Selector(response)

        data = response.xpath('/html/body/div[3]/table/tbody/tr')

        item = SebiventurecapitalfundsItem()

        for i in data:
            item['name'] = i.xpath('.//td[1]/text()').extract_first()
            item['contact_person'] = i.xpath('.//td[3]/text()').extract_first()
            item['email_id'] = i.xpath('.//td[4]/a/text()').extract_first()
            item['address'] = i.xpath('.//td[2]/text()').extract()
            item['platform'] = 'Startup India Fund'
            item['scraped_time'] = datetime.now().strftime('%m/%d/%Y')

            yield item

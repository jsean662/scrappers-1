# -*- coding: utf-8 -*-
import scrapy
from scrapy.selector import Selector
from ..items import SebiventurecapitalfundsItem
from datetime import datetime

class SebiventurecapitalspiderSpider(scrapy.Spider):
    name = "SEBIVentureCapitalSpider"
    allowed_domains = ["sebi.gov.in/"]
    start_urls = [
        'http://www.sebi.gov.in/investor/venturecap.html/',
    ]

    def parse(self, response):
        record = Selector(response)

        data = response.xpath('//*[@id="Web%20upload%20VCFs%20list%20as%20on%20Feb%2001%2C%202011(1)_27363"]/table/tbody/tr')

        item = SebiventurecapitalfundsItem()

        for i in data:
            item['data_id'] = i.xpath('.//td[1]/text()').extract_first()
            item['name'] = i.xpath('.//td[2]/text()').extract_first()
            item['registration_no'] = i.xpath('.//td[3]/text()').extract_first()
            item['date_of_registration'] = i.xpath('.//td[4]/text()').extract_first()
            item['address'] = i.xpath('.//td[5]/text()').extract()
            item['platform'] = 'SEBI Venture Capital'
            item['scraped_time'] = datetime.now().strftime('%m/%d/%Y')

            yield item
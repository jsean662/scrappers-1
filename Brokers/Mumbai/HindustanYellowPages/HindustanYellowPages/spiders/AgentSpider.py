# -*- coding: utf-8 -*-
import scrapy
from ..items import HindustanyellowpagesItem
from datetime import datetime
from scrapy.selector import Selector


class AgentspiderSpider(scrapy.Spider):
    name = "AgentSpider"
    allowed_domains = ["hindustanyellowpages.in"]
    start_urls = [
        'http://www.hindustanyellowpages.in/Mumbai/REAL-ESTATE-AGENT/Page%s' %str(page) for page in range(1, 12)
    ]
    custom_settings = {
        'DOWNLOAD_DELAY': 2.0,
    }

    def parse(self, response):
        item = HindustanyellowpagesItem()

        records = Selector(response).xpath('//*[@id="company_list_grid"]/table[1]/tr')

        # print(records)

        for record in records:
            item['scraped_time'] = datetime.now().strftime('%m/%d/%Y')
            item['platform'] = 'Hindustan Yellow Pages'

            item['name'] = record.xpath('.//th[@id="c_name"]/a/text()').extract_first(default='')
            # print(item['name'])
            item['mobile_no'] = record.xpath('.//table[@id="tabdata"]/tr[contains(@id,"repCompanyDetail_trMobileNo")]//*/a/@href').extract()
            if item['mobile_no']:
                item['mobile_no'] = ','.join(item['mobile_no']).replace('tel:', '').replace(',,', ',')

            # print(item['mobile_no'])
            item['phone_no'] = record.xpath('.//table[@id="tabdata"]/tr[contains(@id,"repCompanyDetail_trOfficeNo")]//*/a/@href').extract()
            if item['phone_no']:
                item['phone_no'] = ','.join(item['phone_no']).replace('tel:', '').replace(',,', ',')

            item['email_id'] = record.xpath('.//tr[contains(@id,"repCompanyDetail_trEmail")]//*/span[@id="comdataspan"]/a/@href').extract()

            if item['email_id']:
                item['email_id'] = ','.join(item['email_id']).replace('mailto:', '').replace(',,', ',')

            item['address'] = record.xpath('.//table[@id="tabdata"]//*/span[contains(@id,"repCompanyDetail_lblAddress")]/text()').extract_first()

            item['website'] = record.xpath('.//table[@id="tabdata"]/tr[contains(@id,"repCompanyDetail_trWebsite")]//*/a/@href').extract_first()

            yield item

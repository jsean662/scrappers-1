# -*- coding: utf-8 -*-
import scrapy
from ..items import PublicsectorinfoItem
from datetime import datetime


class PublicspiderSpider(scrapy.Spider):
    name = "publicSpider"
    allowed_domains = ["http://dpe.gov.in"]
    start_urls = [
        'http://dpe.gov.in/data-bank-officials?title=&field_select_data_bank_category_tid=All&page=%s' %str(page) for page in range(0, 29)
    ]
    custom_settings = {
        # 'ITEM_PIPELINES': {
        #     'PublicSectorInfo.pipelines.GovernmentPipeline': 1
        # },
        # 'FILES_STORE': './PDFs',
        'DOWNLOAD_DELAY': 2,
    }

    def parse(self, response):

        records = response.xpath('//table[@class="views-table cols-7"]/tbody/tr')
        # item['file_urls'] = []

        for member in records:
            item = PublicsectorinfoItem()

            item['position'] = item['name'] = 'None'
            item['name'] = member.xpath('.//td[2]/text()').extract_first(default='').strip()

            item['position'] = member.xpath('.//td[3]/p/text()').extract_first(default='').strip()
            item['organisation'] = 'None'
            if ',' in item['position']:
                item['organisation'] = ', '.join(item['position'].split(',')[1:])

            item['dob'] = member.xpath('.//td[4]/span/text()').extract_first(default='').strip()
            item['mobile_no'] = item['telephone_no'] = '0'

            item['telephone_no'] = member.xpath('.//td[5]/text()').extract_first(default='').strip()
            if ',' in item['telephone_no']:
                item['mobile_no'] = ', '.join(item['telephone_no'].split(',')[1:])
                item['telephone_no'] = item['telephone_no'].split(',')[0]

            item['email_address'] = member.xpath('.//td[6]/text()').extract_first(default='').replace('[at]', '@').replace('[dot]', '.').strip()

            # item['file_urls'] = member.xpath('.//td[last()]/a/@href').extract()

            item['scraped_time'] = datetime.now().strftime('%m/%d/%Y')
            item['platform'] = 'DEPARTMENT OF PUBLIC ENTERPRISES - http://dpe.gov.in/'

            yield item

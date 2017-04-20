# -*- coding: utf-8 -*-
import scrapy
from ..items import AsklailabrokersItem
from datetime import datetime as dt


class AsklailaspiderSpider(scrapy.Spider):
    name = "asklailaSpider"
    allowed_domains = ["www.asklaila.com"]
    start_urls = [
        # 'https://www.asklaila.com/search/Mumbai/mumbai/real-estate-builders-developers/%s/' % str(page) for page in range(10, 240, 10)
        'https://www.asklaila.com/search/Mumbai/mumbai/real-estate-builders-developers/',
    ]
    custom_settings = {
        'DOWNLOAD_DELAY': 3.0,
    }

    def parse(self, response):
        item = AsklailabrokersItem()
        id = 1

        data = response.xpath('//div[@class="col-xs-12  col-sm-12 col-md-6 col-lg-6 cardWrap"]')

        for i in data:
            item['company_name'] = i.xpath('.//h2[@class="resultTitle"]/text()').extract_first(default='None')
            if 'None' in item['company_name']:
                continue
            item['locality'] = i.xpath('./*//div[@class="col-xs-12 col-sm-12 col-md-12 col-lg-12 cardElement"]/div[@class="col-xs-12 col-sm-12 col-md-12 col-lg-12 mar0 pad0"]/text()').extract()
            item['mobile_no'] = i.xpath('./*//label/text()').extract_first(default='0').strip().replace('\t', '').replace('\n', '').replace('x', '').replace('a', '')
            if ',' in item['mobile_no']:
                item['phone_no'] = item['mobile_no'].split(',')[0]
                item['mobile_no'] = item['mobile_no'].split(',')[1]
            else:
                item['phone_no'] = '0'
            item['city'] = 'Mumbai'
            item['scraped_time'] = dt.now().strftime('%m/%d/%Y')
            item['data_id'] = id
            id += 1

            yield item

# -*- coding: utf-8 -*-
import scrapy
from ..items import SmartrealtorsItem
from datetime import datetime as dt
from scrapy.http import Request


class SmartrealtorspiderSpider(scrapy.Spider):
    name = "smartrealtorSpider"
    allowed_domains = ["http://smartrealtors.co.in"]
    start_urls = [
        'http://smartrealtors.co.in/index.php?page=1&option=com_agents&view=basic&Itemid=67#filterform/',
    ]
    custom_settings = {
        'DEPTH_LIMIT': 10000,
        'DOWNLOAD_DELAY': 5.0,
    }

    def parse(self, response):
        members = response.xpath('//div[@class="mem_conatiner"]')

        item = SmartrealtorsItem()

        for i in members:
            item['company_name'] = 'None'
            item['second_name'] = item['broker_name'] = 'None'
            item['mobile_no'] = '0'
            item['phone_no'] = '0'
            item['localities'] = 'None'
            item['city'] = 'Mumbai'
            item['platform'] = 'SmartRealtors'
            item['txn_type'] = 'None'
            item['property_type'] = 'None'
            item['email_id'] = 'None'
            item['second_email'] = 'None'
            item['data_id'] = '0'
            item['website'] = 'None'
            item['description'] = 'None'
            item['scraped_time'] = dt.now().strftime('%m/%d/%Y')

            item['data_id'] = i.xpath('.//div[@class="section_header"]/p[contains(@class,"member")]/text()').extract_first(default='0').strip()

            item['company_name'] = i.xpath('.//div[@class="section_header"]/p[contains(@class,"bombay")]/text()').extract_first(default='None').strip()

            item['description'] = i.xpath('.//div[@class="section_content_1"]/div/p[contains(@class,"desc")]/text()').extract_first(default='None').strip()

            item['website'] = i.xpath('.//div[@class="section_content_1"]/div/p[contains(@class,"website")]/text()').extract_first(default='None').strip()

            item['broker_name'] = i.xpath('.//div[@class="section_content_2"]/div[contains(@class,"t3d1 t3d1right")]/p[2]/span/text()').extract_first(default='None').strip()

            item['mobile_no'] = i.xpath('.//div[@class="section_content_2"]/div[contains(@class,"t3d1 t3d1right")]/p[3]/text()').extract_first(default='0').strip()

            item['email_id'] = i.xpath('.//div[@class="section_content_2"]/div[contains(@class,"t3d1 t3d1right")]/a/text()').extract_first(default='None').strip()

            item['second_name'] = i.xpath('.//div[@class="section_content_2"]/div[contains(@class,"t3d1 t3d1right")]/p[2]/span/text()').extract_first(default='None').strip()

            item['phone_no'] = i.xpath('.//div[@class="section_content_2"]/div[contains(@class,"t3d1 t3d1right")]/p[3]/text()').extract_first(default='0').strip()

            item['second_email'] = i.xpath('.//div[@class="section_content_2"]/div[contains(@class,"t3d1 t3d1right")]/a/text()').extract_first(default='None').strip()

            item['property_type'] = i.xpath('.//div[@class="section_lower"]/div[contains(@class,"section_content_3")]/div[contains(@class,"t4d1")]/p[last()]/span/text()').extract_first(default='None').strip()

            item['txn_type'] = i.xpath('.//div[@class="section_lower"]/div[contains(@class,"section_content_3")]/div[contains(@class,"t4d2")]/p[last()]//span/text()').extract_first(default='None').strip()

            item['localities'] = i.xpath('.//div[@class="section_lower"]/div[contains(@class,"section_content_4")]/div[contains(@class,"t4d3")]/p[2]/text()').extract()

            yield item

        nextURL = response.xpath('//div[contains(@class,"pagination")]/a[contains(text(),"next")]/@href').extract_first(default='None')
        print(nextURL)

        if 'None' in nextURL:
            if 'mem_conatiner' in str(response.body):
                pageno = int(response.url.split('page=')[1].split('&')[0])
                url = response.url.split('page=')[0] + 'page=' + str(pageno+1) + '&' + response.url.split('page=')[1].split('&')[1]
                yield Request(url, callback=self.parse, dont_filter=False)
        else:
            url = 'http://smartrealtors.co.in' + nextURL
            yield Request(url, callback=self.parse, dont_filter=True)

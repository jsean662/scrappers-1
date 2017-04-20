# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request
from ..items import MakaanbrokersItem
from datetime import datetime as dt


class MakaanbrokersmumbaiSpider(scrapy.Spider):
    name = "makaanBrokersMumbai"
    allowed_domains = ["makaan.com"]
    start_urls = [
        'https://www.makaan.com/mumbai/all-real-estate-agent-broker?page=1',
    ]
    custom_settings = {
        'DEPTH_LIMIT': 10000,
        'DOWNLOAD_DELAY': 5,
    }

    def parse(self, response):
        loop = response.xpath('//div[contains(@class,"broker-card")]')
        item = MakaanbrokersItem()

        for i in loop:
            data = i.xpath('.//div/div[contains(@class,"details-wrap")]')
            item['data_id'] = '0'
            item['broker_name'] = 'None'
            item['localities'] = 'None'
            item['total_properties'] = '0'
            item['buy_properties'] = '0'
            item['rent_properties'] = '0'
            item['property_type'] = 'None'
            item['agent_type'] = 'None'
            item['mobile_no'] = '0'
            item['broker_rating'] = 'None'

            item['platfrom'] = 'Makaan'
            item['scraped_time'] = dt.now().strftime('%m/%d/%Y')
            item['city'] = 'Mumbai'

            item['broker_name'] = i.xpath('.//div/div[contains(@class,"profile-wrap")]/div/h2/text()').extract_first(default='None')

            localities_list = data.xpath('.//div[contains(@class,"broker-row clearfix")]/div[contains(@class,"val exco")]/ul[contains(@class,"val-list")]/li/text()').extract()
            if localities_list is None:
                item['localities'] = 'Mumbai'
            else:
                item['localities'] = localities_list

            item['total_properties'] = data.xpath('.//div[contains(@class,"highlights-wrap")]/ul[contains(@class,"hpoint-list")]/li[1]/div[1]/text()').extract_first(default='0')

            item['buy_properties'] = data.xpath('.//div[contains(@class,"highlights-wrap")]/ul[contains(@class,"hpoint-list")]/li[2]/div[1]/text()').extract_first(default='0')

            item['rent_properties'] = data.xpath('.//div[contains(@class,"highlights-wrap")]/ul[contains(@class,"hpoint-list")]/li[3]/div[1]/text()').extract_first(default='0')

            property_type = data.xpath('.//div[3]/div[contains(@class,"val exco")]/ul[contains(@class,"val-list")]/li/h3/text()').extract_first(default='None')

            item['property_type'] = property_type

            item['data_id'] = data.xpath('.//div[contains(@class,"btn-wrap")]/span/@data-companyid').extract_first(default='None')
            item['mobile_no'] = data.xpath('.//div[contains(@class,"btn-wrap")]/span/@data-companyphone').extract_first(default='None')
            item['broker_rating'] = data.xpath('.//div[contains(@class,"btn-wrap")]/span/@data-companyrating').extract_first(default='None')
            item['agent_type'] = data.xpath('.//div[contains(@class,"btn-wrap")]/span/@data-companytype').extract_first(default='None')

            yield item
        pageno = int(response.url.split('page=')[1])
        nexturl = response.xpath('//div[@class="pagination"]/ul/li[last()]/a/@href').extract_first(default='None')
        if 'None' in nexturl:
            if 'broker-card' in str(response.body):
                url = response.url.split(str(pageno))[0] + str(pageno + 1)
                yield Request(url, callback=self.parse, dont_filter=True)
        else:
            url = 'https://www.makaan.com' + nexturl
            yield Request(url, callback=self.parse, dont_filter=True)

# -*- coding: utf-8 -*-
import scrapy
from datetime import datetime
from ..items import Acres99Item
from scrapy.selector import Selector
import re

class AcresspiderSpider(scrapy.Spider):
    name = "AcresSpider"
    allowed_domains = ["www.99acres.com"]
    start_urls = [
        'http://www.99acres.com/property-rates-and-price-trends-in-mumbai',
        'http://www.99acres.com/property-rates-and-price-trends-in-delhi-ncr',
        'http://www.99acres.com/property-rates-and-price-trends-in-chennai',
        'http://www.99acres.com/property-rates-and-price-trends-in-nagpur',
        'http://www.99acres.com/property-rates-and-price-trends-in-gurgaon',
        'http://www.99acres.com/property-rates-and-price-trends-in-hyderabad',
        'http://www.99acres.com/property-rates-and-price-trends-in-vadodara',
        'http://www.99acres.com/property-rates-and-price-trends-in-noida',
        'http://www.99acres.com/property-rates-and-price-trends-in-pune',
        'http://www.99acres.com/property-rates-and-price-trends-in-chandigarh',
        'http://www.99acres.com/property-rates-and-price-trends-in-greater-noida',
        'http://www.99acres.com/property-rates-and-price-trends-in-kolkata',
        'http://www.99acres.com/property-rates-and-price-trends-in-jaipur',
        'http://www.99acres.com/property-rates-and-price-trends-in-ghaziabad',
        'http://www.99acres.com/property-rates-and-price-trends-in-ahmedabad',
        'http://www.99acres.com/property-rates-and-price-trends-in-lucknow',
        'http://www.99acres.com/property-rates-and-price-trends-in-faridabad',
        'http://www.99acres.com/property-rates-and-price-trends-in-bhubaneswar',
        'http://www.99acres.com/property-rates-and-price-trends-in-surat',
        'http://www.99acres.com/property-rates-and-price-trends-in-coimbatore',
        'http://www.99acres.com/property-rates-and-price-trends-in-bangalore',
        'http://www.99acres.com/property-rates-and-price-trends-in-indore',
    ]

    def parse(self, response):
        item = Acres99Item()
        records = Selector(response).xpath('//table[@class="prTble"]/tbody/tr')

        for record in records:
            item['locality'] = record.xpath('.//td[1]/text()').extract_first(default='')

            price = record.xpath('.//td[2]/text()').extract_first(default='').replace(',', '').replace('/sq. ft.', '')
            # print(price)
            if ' - ' in price:
                item['sale_lowest_price'] = price.split('-')[0].strip()
                item['sale_highest_price'] = price.split('-')[1].strip()
            else:
                item['sale_highest_price'] = item['sale_lowest_price'] = price

            rent_lowest_price = record.xpath('.//td[5]/text()').extract_first(default='').replace(',', '').strip()
            if rent_lowest_price == '-':
                rent_lowest_price = record.xpath('.//td[6]/text()').extract_first(default='').replace(',', '').strip()
            if rent_lowest_price == '-':
                rent_lowest_price = record.xpath('.//td[7]/text()').extract_first(default='').replace(',', '').strip()

            if ' - ' in rent_lowest_price:
                item['rent_lowest_price'] = rent_lowest_price.split(' -')[0].strip()
            else:
                item['rent_lowest_price'] = rent_lowest_price

            rent_highest_price = record.xpath('.//td[last()]/text()').extract_first(default='').replace(',', '').strip()
            if rent_highest_price == '-':
                rent_highest_price = record.xpath('.//td[6]/text()').extract_first(default='').replace(',', '').strip()
            if rent_highest_price == '-':
                rent_highest_price = record.xpath('.//td[5]/text()').extract_first(default='').replace(',', '').strip()

            if ' - ' in rent_highest_price:
                item['rent_highest_price'] = rent_highest_price.split('- ')[1].strip()
            else:
                item['rent_highest_price'] = rent_highest_price

            item['scraped_time'] = datetime.now().strftime('%m/%d/%Y')
            item['city'] = response.url.split('in-')[1].replace('-', '')

            yield item

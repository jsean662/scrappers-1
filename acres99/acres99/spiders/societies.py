import scrapy
from ..items import Acres99Item
from scrapy.selector import Selector
import re


class SocietiesSpider(scrapy.Spider):
    name = "societies"
    allowed_domains = ["http://www.99acres.com/property-rates-and-price-trends-in-societies-in-mumbai"]
    start_urls = (
        'http://www.99acres.com/property-rates-and-price-trends-in-societies-in-delhi-ncr',
        'http://www.99acres.com/property-rates-and-price-trends-in-societies-in-chennai',
        'http://www.99acres.com/property-rates-and-price-trends-in-societies-in-nagpur',
        'http://www.99acres.com/property-rates-and-price-trends-in-societies-in-gurgaon',
        'http://www.99acres.com/property-rates-and-price-trends-in-societies-in-hyderabad',
        'http://www.99acres.com/property-rates-and-price-trends-in-societies-in-vadodara',
        'http://www.99acres.com/property-rates-and-price-trends-in-societies-in-noida',
        'http://www.99acres.com/property-rates-and-price-trends-in-societies-in-pune',
        'http://www.99acres.com/property-rates-and-price-trends-in-societies-in-chandigarh',
        'http://www.99acres.com/property-rates-and-price-trends-in-societies-in-greater-noida',
        'http://www.99acres.com/property-rates-and-price-trends-in-societies-in-kolkata',
        'http://www.99acres.com/property-rates-and-price-trends-in-societies-in-jaipur',
        'http://www.99acres.com/property-rates-and-price-trends-in-societies-in-ghaziabad',
        'http://www.99acres.com/property-rates-and-price-trends-in-societies-in-ahmedabad',
        'http://www.99acres.com/property-rates-and-price-trends-in-societies-in-lucknow',
        'http://www.99acres.com/property-rates-and-price-trends-in-societies-in-faridabad',
        'http://www.99acres.com/property-rates-and-price-trends-in-societies-in-bhubaneswar',
        'http://www.99acres.com/property-rates-and-price-trends-in-societies-in-surat',
        'http://www.99acres.com/property-rates-and-price-trends-in-societies-in-mumbai',
        'http://www.99acres.com/property-rates-and-price-trends-in-societies-in-coimbatore',
        'http://www.99acres.com/property-rates-and-price-trends-in-societies-in-bangalore',
        'http://www.99acres.com/property-rates-and-price-trends-in-indore',
    )
    custom_settings = {
        'DEPTH_LIMIT': 10000,
        'DOWNLOAD_DELAY': 5}

    def parse(self, response):
        record = Selector(response)

        data = record.xpath('//table[@class="prTble"]/tbody/tr')

        for i in data:
            item = Acres99Item()


            item['city'] = response.xpath('//h1[@class="mt10 f18 b vp5"]/text()').extract_first()[32:]

            try:
                soc_name = i.xpath('./td[1]/text()').extract_first(default='')
                item['locality_name'] = soc_name.split(',')[1][1:]
                item['society_name'] = soc_name.split(',')[0]
                if (item['society_name'] == '') or (item['society_name'] == ' '):
                    item['society_name'] = 'None'
            except:
                item['society_name'] = 'None'
                item['locality_name'] = 'None'

            try:
                sqft_per = i.xpath('./td[2]/text()').extract_first(default=0)
                if not (sqft_per is None):
                    sqft_per = sqft_per.replace('/sq. ft.', '').replace(',', '')
                    item['lower_price'] = sqft_per.split('-')[0]
                    item['upper_price'] = sqft_per.split('-')[1]

                if(sqft_per == '-') or (sqft_per == ''):
                    item['lower_price'] = 0
                    item['upper_price'] = 0
            except:
                item['lower_price'] = 0
                item['upper_price'] = 0

            item['platform'] = '99 Acres'
            item['date'] = '12/12/2016'

            yield item

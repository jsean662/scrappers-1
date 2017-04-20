# -*- coding: utf-8 -*-
import scrapy
from ..items import MagicpricesItem
from scrapy.http import Request
from scrapy.selector import Selector


class PricebotSpider(scrapy.Spider):
    name = 'pricebot'
    start_urls = [
        'http://www.magicbricks.com/Property-Rates-Trends/ALL-RESIDENTIAL-rates-in-Navi-Mumbai/Page-1',
        'http://www.magicbricks.com/Property-Rates-Trends/ALL-COMMERCIAL-rates-in-Navi-Mumbai/Page-1',
        # 'http://www.magicbricks.com/Property-Rates-Trends/ALL-RESIDENTIAL-rates-in-Thane/Page-1',
        # 'http://www.magicbricks.com/Property-Rates-Trends/ALL-COMMERCIAL-rates-in-Thane/Page-1',
        # 'http://www.magicbricks.com/Property-Rates-Trends/ALL-RESIDENTIAL-rates-in-New-Delhi/Page-1',
        # 'http://www.magicbricks.com/Property-Rates-Trends/ALL-COMMERCIAL-rates-in-New-Delhi/Page-1',
        # 'http://www.magicbricks.com/Property-Rates-Trends/ALL-RESIDENTIAL-rates-in-Mumbai/Page-1',
        # 'http://www.magicbricks.com/Property-Rates-Trends/ALL-COMMERCIAL-rates-in-Mumbai/Page-1',
        # 'http://www.magicbricks.com/Property-Rates-Trends/ALL-RESIDENTIAL-rates-in-Gurgaon/Page-1',
        # 'http://www.magicbricks.com/Property-Rates-Trends/ALL-COMMERCIAL-rates-in-Gurgaon/Page-1',
        # 'http://www.magicbricks.com/Property-Rates-Trends/ALL-RESIDENTIAL-rates-in-Noida/Page-1',
        # 'http://www.magicbricks.com/Property-Rates-Trends/ALL-COMMERCIAL-rates-in-Noida/Page-1',
        # 'http://www.magicbricks.com/Property-Rates-Trends/ALL-RESIDENTIAL-rates-in-Bangalore/Page-1',
        # 'http://www.magicbricks.com/Property-Rates-Trends/ALL-COMMERCIAL-rates-in-Bangalore/Page-1',
        # 'http://www.magicbricks.com/Property-Rates-Trends/ALL-RESIDENTIAL-rates-in-Chennai/Page-1',
        # 'http://www.magicbricks.com/Property-Rates-Trends/ALL-COMMERCIAL-rates-in-Chennai/Page-1',
        # 'http://www.magicbricks.com/Property-Rates-Trends/ALL-RESIDENTIAL-rates-in-Hyderabad/Page-1',
        # 'http://www.magicbricks.com/Property-Rates-Trends/ALL-COMMERCIAL-rates-in-Hyderabad/Page-1',
        # 'http://www.magicbricks.com/Property-Rates-Trends/ALL-RESIDENTIAL-rates-in-Pune/Page-1',
        # 'http://www.magicbricks.com/Property-Rates-Trends/ALL-COMMERCIAL-rates-in-Pune/Page-1',
        # 'http://www.magicbricks.com/Property-Rates-Trends/ALL-RESIDENTIAL-rates-in-Kolkata/Page-1',
        # 'http://www.magicbricks.com/Property-Rates-Trends/ALL-COMMERCIAL-rates-in-Kolkata/Page-1',
        # 'http://www.magicbricks.com/Property-Rates-Trends/ALL-RESIDENTIAL-rates-in-Ahmedabad/Page-1',
        # 'http://www.magicbricks.com/Property-Rates-Trends/ALL-COMMERCIAL-rates-in-Ahmedabad/Page-1',
        # 'http://www.magicbricks.com/Property-Rates-Trends/ALL-RESIDENTIAL-rates-in-Chandigarh/Page-1',
        # 'http://www.magicbricks.com/Property-Rates-Trends/ALL-COMMERCIAL-rates-in-Chandigarh/Page-1',
        # 'http://www.magicbricks.com/Property-Rates-Trends/ALL-RESIDENTIAL-rates-in-Lucknow/Page-1',
        # 'http://www.magicbricks.com/Property-Rates-Trends/ALL-COMMERCIAL-rates-in-Lucknow/Page-1',
        # 'http://www.magicbricks.com/Property-Rates-Trends/ALL-RESIDENTIAL-rates-in-Jaipur/Page-1',
        # 'http://www.magicbricks.com/Property-Rates-Trends/ALL-COMMERCIAL-rates-in-Jaipur/Page-1',
        # 'http://www.magicbricks.com/Property-Rates-Trends/ALL-RESIDENTIAL-rates-in-Kochi/Page-1',
        # 'http://www.magicbricks.com/Property-Rates-Trends/ALL-COMMERCIAL-rates-in-Kochi/Page-1',
        # 'http://www.magicbricks.com/Property-Rates-Trends/ALL-RESIDENTIAL-rates-in-Indore/Page-1',
        # 'http://www.magicbricks.com/Property-Rates-Trends/ALL-COMMERCIAL-rates-in-Indore/Page-1',
        # 'http://www.magicbricks.com/Property-Rates-Trends/ALL-RESIDENTIAL-rates-in-Coimbatore/Page-1',
        # 'http://www.magicbricks.com/Property-Rates-Trends/ALL-COMMERCIAL-rates-in-Coimbatore/Page-1',
    ]

    custom_settings = {
        'DEPTH_LIMIT': 10000,
        'DOWNLOAD_DELAY': 5,
    }

    def parse(self, response):
        hxs = Selector(response)
        item = MagicpricesItem()

        for i in range(1, 21):
            item['area_name'] = hxs.xpath('//tbody[@id="localitySec"]/tr[' + str(i) + ']/td/a/text()').extract_first(default='-')
            item['sale_price_range'] = hxs.xpath('//div[@id="saleTable"]/table/tr[' + str(i + 2) + ']/td[1]/text()').extract_first(default='-')
            item['sale_avg_price'] = hxs.xpath('//div[@id="saleTable"]/table/tr[' + str(i + 2) + ']/td[2]/text()').extract_first(default='-')
            item['rent_price_range'] = hxs.xpath('//div[@id="rentTable"]/table/tr[' + str(i + 2) + ']/td[1]/text()').extract_first(default='-')
            item['rent_avg_price'] = hxs.xpath('//div[@id="rentTable"]/table/tr[' + str(i + 2) + ']/td[2]/text()').extract_first(default='-')
            if 'RESIDENTIAL' in str(response.url):
                item['property_type'] = 'RESIDENTIAL'
            elif 'COMMERCIAL' in str(response.url):
                item['property_type'] = 'COMMERCIAL'
            item['city'] = response.url.split('-')[-2].split('/')[0]
            yield item

        cur = int(response.url.split('-')[-1])
        if 'trends-pagination' in str(response.body):
            next_url = '-'.join(response.url.split('-')[:-1]) + '-' + str(cur + 1)
            yield Request(next_url, callback=self.parse, dont_filter=False)

        # if 'RESIDENTIAL' in str(response.url):
        # if 'COMMERCIAL' in str(response.url):
        #     cur = int(response.url.split('-')[-1])
        #     if 'trends-pagination' in str(response.body):
        #         next_url = '-'.join(response.url.split('-')[:-1]) + '-' + str(cur + 1)
        #         yield Request(next_url, callback=self.parse)

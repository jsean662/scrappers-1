# -*- coding: utf-8 -*-
import scrapy
from ..items import MakaanItem
from scrapy.http import Request
from scrapy.selector import Selector
import re
from datetime import datetime


class PricespiderSpider(scrapy.Spider):
    name = "MakaanSpider"
    allowed_domains = ["www.makaan.com"]
    start_urls = [
        'https://www.makaan.com/price-trends',
        # 'https://www.makaan.com/price-trends/property-rates-for-rent-in-ahmedabad',
    ]
    custom_settings = {
        'DOWNLOAD_DELAY': 3.0,
    }

    def parse(self, response):
        citylinks = Selector(response).xpath('//div[@id="city_apartment"]/table[@class="tbl"]/tbody/tr/td[1]/a/@href').extract()
        # print(citylinks)

        for link in citylinks:
            url = 'https://www.makaan.com/' + link
            # print(url)
            yield Request(url, callback=self.sale, dont_filter=False)
            yield Request(url.replace('buy', 'rent'), callback=self.rent, dont_filter=False)

    def sale(self, response):
        item = MakaanItem()

        records = response.xpath('//*[@id="locality_apartment"]/table/tbody/tr')

        for record in records:
            try:
                item['locality'] = record.xpath('.//td[1]/a/span/text()').extract_first()
                item['lowest_price'] = re.findall('[0-9]+', record.xpath('.//td[2]/span[1]/text()').extract_first(default=''))[0:]
                item['highest_price'] = re.findall('[0-9]+', record.xpath('.//td[2]/span[2]/text()').extract_first(default=''))[0:]
                item['city'] = response.url.split('in-')[1].split('?')[0]
                if '?' in item['city']:
                    item['city'] = item['city'].split('?')[0]
                item['txn_type'] = 'Sale'
                item['scraped_time'] = datetime.now().strftime('%m/%d/%Y')
                item['middle_price'] = '0'
            except:
                pass
            finally:
                yield item
        url = Selector(response).xpath('*//div[@class="pagination"]/ul/li[last()]/a/@href').extract_first()
        if url is None:
            pass
        else:
            yield Request('https://www.makaan.com/'+url, callback=self.sale, dont_filter=False)

    def rent(self, response):
        item = MakaanItem()
        records = response.xpath('//*[@id="locality_apartment"]/tbody/tr')
        print(records)

        for record in records:
            try:
                item['locality'] = record.xpath('.//td[1]/a/span/text()').extract_first(default='')

                lowest_price = record.xpath('.//td[2]/span/text()').extract()
                if lowest_price:
                    lowest_price = lowest_price[0]
                    if lowest_price == '' or lowest_price == ' ' or lowest_price == None:
                        lowest_price = lowest_price[1]
                        if 'L' in lowest_price:
                            lowest_price = str(eval(re.findall('[0-9]+', lowest_price.split(' L')[0])[0]) * 100000)
                        else:
                            lowest_price = ''.join(re.findall('[0-9]+', lowest_price))
                    else:
                        if 'L' in lowest_price:
                            lowest_price = str(eval(re.findall('[0-9]+', lowest_price.split(' L')[0])[0]) * 100000)
                        else:
                            lowest_price = ''.join(re.findall('[0-9]+', lowest_price))
                else:
                    lowest_price = ''
                item['lowest_price'] = lowest_price.strip().replace(',', '')

                middle_price = record.xpath('.//td[4]/span/text()').extract()
                if middle_price:
                    middle_price = middle_price[0]
                    if middle_price == '' or middle_price == ' ' or middle_price == None:
                        middle_price = middle_price[1]
                        if 'L' in middle_price:
                            middle_price = str(eval(re.findall('[0-9]+', middle_price.split(' L')[0])[0]) * 100000)
                        else:
                            middle_price = ''.join(re.findall('[0-9]+', middle_price))
                    else:
                        if 'L' in middle_price:
                            middle_price = str(eval(re.findall('[0-9]+', middle_price.split(' L')[0])[0]) * 100000)
                        else:
                            middle_price = ''.join(re.findall('[0-9]+', middle_price))
                else:
                    middle_price = ''

                item['middle_price'] = middle_price.strip().replace(',', '')

                highest_price = record.xpath('.//td[6]/span/text()').extract()
                if highest_price:
                    highest_price = highest_price[0]
                    if highest_price == '' or highest_price == ' ' or highest_price == None:
                        highest_price = highest_price[1]
                        if 'L' in highest_price:
                            highest_price = str(eval(re.findall('[0-9]+', highest_price.split(' L')[0])[0]) * 100000)
                        else:
                            highest_price = ''.join(re.findall('[0-9]+', highest_price))
                    else:
                        if 'L' in highest_price:
                            highest_price = str(eval(re.findall('[0-9]+', highest_price.split(' L')[0])[0]) * 100000)
                        else:
                            highest_price = ''.join(re.findall('[0-9]+', highest_price))
                else:
                    highest_price = ''
                item['highest_price'] = highest_price.strip().replace(',', '')

                item['city'] = response.url.split('in-')[1].split('?')[0]
                if '?' in item['city']:
                    item['city'] = item['city'].split('?')[0]
                item['txn_type'] = 'Rent'
                item['scraped_time'] = datetime.now().strftime('%m/%d/%Y')
            except:
                pass
            finally:
                yield item
        url = response.xpath('*//div[@class="pagination"]/ul/li[last()]/a/@href').extract_first()
        if url is None:
            pass
        else:
            yield Request('https://www.makaan.com/'+url, callback=self.rent, dont_filter=False)

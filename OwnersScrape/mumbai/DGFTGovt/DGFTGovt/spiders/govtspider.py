# -*- coding: utf-8 -*-
import scrapy
from ..items import DgftgovtItem


class GovtspiderSpider(scrapy.Spider):
    name = "govtspider"
    allowed_domains = ["dgft.gov.in"]
    start_urls = [
        'http://dgft.gov.in/dgftmumbai/html/StatusHolderList.htm',
    ]

    def parse(self, response):
        item = DgftgovtItem()

        data = response.xpath('//table[@width="100%"]/tbody/tr')

        for i in data:
            item['name'] = 'None'
            item['email'] = 'None'
            item['mobile_no'] = '0'
            item['address'] = []
            item['index_no'] = '0'
            item['type'] ='None'
            item['valid_date'] = '0'
            item['certification_no'] = '0'
            
            item['index_no'] = i.xpath('.//td[1]/text()').extract_first(default='0').strip()
            info = i.xpath('.//td[2]/text()').extract()
            if info is not None:
                info = [s.strip() for s in info]
                info = [s.replace('\r', '').replace('\n', '').replace('  ', '') for s in info]
                item['name'] = info[0].strip()
                item['address'] = info[1:(len(info)-2)]
                item['mobile_no'] = info[len(info)-2].strip()
                item['email'] = info[len(info) - 1].strip()
            item['type'] = i.xpath('.//td[3]/text()').extract_first(default='0').strip()
            item['valid_date'] = i.xpath('.//td[4]/text()').extract_first(default='0').strip()
            item['certification_no'] = i.xpath('.//td[5]/text()').extract_first(default='0').strip()

            if item['name'] == '' or item['name'] == ' ' or item['name'] == 'NIL':
                item['name'] = 'None'

            if item['email'] == '' or item['email'] == ' ' or item['email'] == 'NIL':
                item['email'] = 'None'

            if item['mobile_no'] == '' or item['mobile_no'] == ' ' or item['mobile_no'] == 'NIL':
                item['mobile_no'] = '0'

            yield item

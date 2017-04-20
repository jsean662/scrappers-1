# -*- coding: utf-8 -*-
import scrapy
from ..items import TheyellowpageItem
from datetime import datetime


class AgentsspiderSpider(scrapy.Spider):
    name = "AgentsSpider"
    allowed_domains = ["theyellowpages.in"]
    start_urls = [
        'http://www.theyellowpages.in/search-result.aspx?city=Mumbai&cid=849&pid=3622&area=&Page=%s' % str(page) for page in range(1, 15)
    ]

    def parse(self, response):
        records = response.xpath('//*[@id="listing"]/table')

        item = TheyellowpageItem()
        for record in records:
            item['platform'] = 'The Yellow Pages.in'
            item['scraped_time'] = datetime.now().strftime('%m/%d/%Y')

            item['company_name'] = record.xpath('.//tr/td[2]/p[1]/span/a/text()').extract_first(default='').replace('\r', '').replace('\n', '').strip()
            item['mobile_no'] = item['phone_no'] = item['address'] = ''

            data = record.xpath('.//tr/td[2]/p[1]/text()').extract()
            if data:
                length = len(data)
                if length >= 8:
                    item['mobile_no'] = data[4]
                    # record.xpath('.//tr/td[2]/p[1]/text()[2]').extract_first()
                    item['phone_no'] = data[3]
                    # record.xpath('.//tr/td[2]/p[1]/text()[1]').exrtact_first()
                    item['address'] = data[5:]
                else:
                    item['mobile_no'] = ''
                    # record.xpath('.//tr/td[2]/p[1]/text()[2]').extract_first()
                    item['phone_no'] = data[3]
                    # record.xpath('.//tr/td[2]/p[1]/text()[1]').exrtact_first()
                    item['address'] = data[4:]

                for a in item['address']:
                    a = a.replace('\r', '').replace('\n', '').replace('  ', ' ')
                    item['address'].append(a.strip())
            yield item

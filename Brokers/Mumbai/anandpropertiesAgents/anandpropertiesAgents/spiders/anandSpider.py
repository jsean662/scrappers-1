# -*- coding: utf-8 -*-
import scrapy
from ..items import AnandpropertiesagentsItem
from scrapy.selector import Selector


class AnandspiderSpider(scrapy.Spider):
    name = "anandSpider"
    allowed_domains = ["www.anandproperties.com"]
    start_urls = [
        'https://www.anandproperties.com/mumbai/real-estate-agents.php/',
        'https://www.anandproperties.com/mumbai/real-estate-agents.php?pageno=2',
        'https://www.anandproperties.com/mumbai/real-estate-agents.php?pageno=3',
        'https://www.anandproperties.com/mumbai/real-estate-agents.php?pageno=4',
        'https://www.anandproperties.com/mumbai/real-estate-agents.php?pageno=5',
        'https://www.anandproperties.com/mumbai/real-estate-agents.php?pageno=6',
        'https://www.anandproperties.com/mumbai/real-estate-agents.php?pageno=7',
        'https://www.anandproperties.com/mumbai/real-estate-agents.php?pageno=8',
        # 'https://www.anandproperties.com/mumbai/pg-providers.php',
        # 'https://www.anandproperties.com/mumbai/architects.php'
    ]

    def parse(self, response):
        record = Selector(response)
        item = AnandpropertiesagentsItem()

        data = record.xpath('//tr[@align="left"]')
        for i in data:
            item['data_id'] = i.xpath('.//td[1]/text()').extract_first(default='0')
            item['company_name'] = i.xpath('.//td[2]/a/text()').extract_first(default='None')
            item['broker_name'] = i.xpath('.//td[3]/text()').extract_first(default='None')
            mobile_no = i.xpath('.//td[4]/text()').extract()

            if len(mobile_no) > 1:
                item['phone_no'] = mobile_no[0]
                item['mobile_no'] = ','.join(mobile_no[1:])


            item['description'] = i.xpath('.//td[5]/text()').extract_first(default='None')
            item['address'] = i.xpath('.//td[3]/text()').extract()

            yield item

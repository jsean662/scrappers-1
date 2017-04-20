# -*- coding: utf-8 -*-
import scrapy
from datetime import datetime
from ..items import ZricksItem
from scrapy.selector import Selector
from scrapy.http import Request


class ZricksspiderSpider(scrapy.Spider):
    name = "zricksSpider"
    allowed_domains = ["www.zricks.com"]
    start_urls = [
        'https://www.zricks.com/AgentsCompany/',
    ]

    def parse(self, response):
        record = Selector(response)

        brokers = record.xpath('//div[@id="sectionA_1"]/div[2]/div[2]/div/div[1]/div/div[contains(@class,"row margin-top-20")]')
        item = ZricksItem()
        for broker in brokers:
            item['company_name'] = broker.xpath('./*//div[@class="media"]/div[@class="media-body"]/h2/a/text()').extract_first()
            item['email_id'] = broker.xpath('./*//div[@class="media"]/div[@class="media-body"]/span[@class="wraptext"]/a/span/text()').extract_first()

            item['scraped_time'] = datetime.now().strftime('%m/%d/%Y')
            item['platform'] = 'Zricks'

            yield item
        nurl = record.xpath('//*[@id="ContentPlaceHolder1_ListView1_DataPager1"]/a[contains(text(),"Next")]/@href').extract_first(default='None')

        url = 'https://www.zricks.com' + nurl
        yield Request(url, callback=self.parse, dont_filter=False)

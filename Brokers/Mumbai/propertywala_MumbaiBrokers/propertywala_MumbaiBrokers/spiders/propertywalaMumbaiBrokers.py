# -*- coding: utf-8 -*-
import scrapy
from scrapy.selector import Selector
from ..items import PropertywalaMumbaibrokersItem


class PropertywalamumbaibrokersSpider(scrapy.Spider):
    name = "propertywalaMumbaiBrokers"
    allowed_domains = ["propertywala.com"]
    start_urls = [
        'https://www.propertywala.com/directory/type-residential/location-mumbai_maharashtra/postedby-broker?page=%s' % page for page in range(1, 21)
    ]
    custom_settings = {
        "ITEM_PIPELINES": {'scrapy.pipelines.images.ImagesPipeline': 1},
        "IMAGES_STORE": './Agents',
        'DEPTH_LIMIT': 10000,
        'DOWNLOAD_DELAY': 5,
    }

    def parse(self, response):
        try:
            record = Selector(response)

            # agents = record.xpath('//article[contains(@id,"U")]')

            item = PropertywalaMumbaibrokersItem()

            # for i in agents:
            item['image_urls'] = response.xpath('//article[contains(@id,"U")]/figure/a/img/@src').extract()
            # print(item['image_urls'])
            # item['image'] = [item['image_urls']]

            yield item
        except Exception as e:
            print(e)

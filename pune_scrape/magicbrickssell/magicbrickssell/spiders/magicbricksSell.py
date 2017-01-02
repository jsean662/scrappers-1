import scrapy
import logging
from scrapy.spiders import Spider
from scrapy.spiders import CrawlSpider, Rule
from scrapy.selector import Selector
from scrapy.http import Request
from datetime import datetime as dt
from datetime import time,timedelta
from datetime import date
import time
import sys
import re
from magicbrickssell.items import MagicbrickssellItem

class MagicbricksSell(CrawlSpider):
	name = 'magicbrickssellSpider'
	start_urls = ['http://www.magicbricks.com/property-for-sale/residential-real-estate?proptype=Multistorey-Apartment,Builder-Floor-Apartment,Penthouse,Studio-Apartment,Residential-House,Villa&cityName=Pune/Page-1']
	custom_settings = {
		'DEPTH_LIMIT' : 10000 ,
		'DOWNLOAD_DELAY' : 5 ,
	}

	item = MagicbrickssellItem()

	def parse(self,response):
		hxs = Selector(response)

		data = hxs.xpath('//div[contains(@id,"resultBlockWrapper")]')

		for i in data:
			ids = i.xpath('@id').extract_first()
			self.item['data_id'] = re.findall('[0-9]+',ids)[0]

			self.item['txn_type'] = i.xpath('.//input[contains(@id,"transactionType")]/@value').extract_first()

			yield self.item
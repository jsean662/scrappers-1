import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.selector import Selector
from scrapy.http import Request
from scrapy.linkextractors import LinkExtractor
from scrapy.selector import Selector
from abode.items import AbodeItem
from scrapy.http import FormRequest
from scrapy.utils.response import open_in_browser

class AbodeSpider(CrawlSpider):
	name = "abode"
	allowed_domains = ["abodesindia.com"]
	start_urls = ["http://www.abodesindia.com/property-for-sale-all-residential-in-mumbai/1101#"]

	custom_settings = {	'BOT_NAME': 'abode-scraper',
						'DEPTH_LIMIT': 1000,
						'DOWNLOAD_DELAY': 4
						}
	def parse(self , response):
		hxs = Selector(response)

		#print response.body
		data = hxs.xpath('//div[@style="border:1px solid #CCC; "]')
		print data
		for i in data:
			item = AbodeItem()

    		item['data_id'] = i.xpath('div[1]/div[1]/span/text()').extract()
    		yield item
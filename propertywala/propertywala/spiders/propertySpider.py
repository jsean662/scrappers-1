import scrapy
from scrapy import log
from scrapy.spiders import Spider
from scrapy.http import Request
from scrapy.exceptions import CloseSpider
from scrapy.spiders import CrawlSpider, Rule
from scrapy.selector import Selector
from scrapy.http import Request
from propertywala.items import PropertywalaItem
from scrapy.loader import ItemLoader
import time
from datetime import date
class PropWala(CrawlSpider):
	name = "propertyWalaSpider"
	allowed_domains = ['propertywala.com']
	start_urls = [ "https://www.propertywala.com/properties/type-residential/for-sale/location-mumbai_maharashtra","https://www.propertywala.com/properties/type-residential/for-rent/location-mumbai_maharashtra"
		#"https://www.propertywala.com/properties/type-commercial/for-rent/location-mumbai_maharashtra?page=1",
		#"https://www.propertywala.com/properties/type-commercial/for-sale/location-mumbai_maharashtra?page=1"
		]      
	
	item = PropertywalaItem()

	def parse(self, response):
		hxs = Selector(response)
		data = hxs.xpath('//li[@class="posted"]')

		for i in data:
			'''
			Extracting the urls for each property and jump to new page of that property
			'''
			url = 'https://www.propertywala.com/'+i.xpath('text()').extract_first().strip().encode('ascii', 'ignore').decode('ascii').replace('ID: ','').replace('  Posted:','')
			
			yield Request(url,callback=self.parse1,dont_filter=True)

		next = response.xpath('//div[@class="paging"]/a[last()-1]/@href').extract_first()
		if (not '?' in str(response.url)):
			maxPage = int(response.xpath('//div[@class="paging"]/a[last()]/@href').extract_first().split('=')[-1])
		if (not next==None):
			next_url = 'https://www.propertywala.com/'+next
			#print "+++++++++++++++++++++++++++++++"
			#print next_url
			#print "+++++++++++++++++++++++++++++++"
			#yield Request(next_url,callback=self.parse)

	def parse1(self,response):
		hxs = Selector(response)
		
		self.item['data_id'] = response.url.split('/')[-1]

		if 'sale' in str(response.url):
			self.item['txn_type'] = 'Sale'
		if 'rent' in str(response.url):
			self.item['txn_type'] = 'Rent'

		detail = response.xpath('//ul[@id="PropertyAttributes"]/li/text()').extract()
		print detail
		

		value = response.xpath('//ul[@id="PropertyAttributes"]/li/span/text()').extract()
		print value

		self.item['listing_date'] = response.xpath('//li[@class="noPrint"]/time/@datetime').extract_first().replace('Z','')
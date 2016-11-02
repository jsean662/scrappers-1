import scrapy
import logging
from bookmyflat.items import BookmyflatItem
from scrapy.spiders import Spider
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.selector import Selector
from scrapy.http import Request
from urlparse import urljoin
from datetime import datetime as dt
from datetime import time,timedelta
from datetime import date
import time
import re

class BookFlat(CrawlSpider):
	name = 'bookmySpider'
	start_urls = ['http://bookmyflat.com/properties-search-results/page/2/?sort=newest&search_city=Mumbai&search_lat&search_lng&search_category=0&search_type=0']
	item = BookmyflatItem()
	page=1
	
	def parse(self,response):
		hxs = Selector(response)

		data = hxs.xpath('//a[@class="card"]')

		for i in data:
			
			self.item['lat'] = '0'
			self.item['longt'] = '0'
			self.item['Bua_sqft'] = '0'
			self.item['carpet_area'] = '0'
			self.item['price_per_sqft'] = '0'
			self.item['Selling_price'] = '0'
			self.item['Monthly_Rent'] = '0'
			self.item['management_by_landlord'] = 'None'
			self.item['areacode'] = 'None'
			self.item['mobile_lister'] = 'None'
			self.item['google_place_id'] = 'None'
			self.item['Launch_date'] = '0'
			self.item['Possession'] = '0'
			self.item['age'] = 'None'
			self.item['address'] = 'None'
			self.item['price_on_req'] = 'None'
			self.item['sublocality'] = 'None'
			self.item['config_type'] = 'None'
			self.item['txn_type'] = 'None'
			self.item['property_type'] = 'None'
			self.item['Building_name'] = 'None'
			self.item['locality'] = 'None'
			self.item['Status'] = 'None'
			self.item['listing_by'] = 'None'
			self.item['name_lister'] = 'None'
			self.item['Details'] = 'None'
			self.item['data_id'] = 'None'
			self.item['listing_date'] = dt.now().strftime('%m/%d/%Y %H:%M:%S')
			self.item['updated_date'] = self.item['listing_date']

			self.item['property_type'] = 'Residential'
			self.item['city'] = 'Mumbai'
			self.item['platform'] = 'Bookmyflat'

			self.item['data_id'] = i.xpath('@id').extract_first().split('-')[-1]

			try:
				self.item['txn_type'] = i.xpath('div[@class="figure"]/div[@class="figType"]/text()').extract_first().split()[-1]
			except:
				self.item['txn_type'] = 'None'
				print 'No type'

			self.item['Building_name'] = i.xpath('h2/text()').extract_first()

			self.item['address'] = i.xpath('div[@class="cardAddress"]/text()').extract()
			self.item['address'] = ''.join(self.item['address']).strip()

			if 'ale' in self.item['txn_type']:
				pr = i.xpath('div[@class="cardAddress"]/div/b/text()').extract_first()
				self.item['Selling_price'] = re.findall('[^a-zA-Z,.]+',pr)
				self.item['Selling_price'] = ''.join(self.item['Selling_price'])
				self.item['Monthly_Rent'] = '0'
			if 'ent' in self.item['txn_type']:
				pr = i.xpath('div[@class="cardAddress"]/div/b/text()').extract_first()
				self.item['Monthly_Rent'] = re.findall('[^a-zA-Z,.]+',pr)
				self.item['Monthly_Rent'] = ''.join(self.item['Monthly_Rent'])
				self.item['Selling_price'] = '0'
			if self.item['txn_type']=='None':
				if not self.item['Selling_price']=='0':
					self.item['txn_type'] = 'Sale'
				if not self.item['Monthly_Rent']=='0':
					self.item['txn_type'] = 'Rent'

			try:
				self.item['config_type'] = i.xpath('ul[@class="cardFeat"]/li[1]/text()').extract_first().strip()+'BHK'
			except:
				self.item['config_type'] = '0'

			self.item['listing_date'] = dt.now().strftime('%m/%d/%Y %H:%M:%S')
			self.item['updated_date'] = self.item['listing_date']

			try:
				sqf = i.xpath('ul[@class="cardFeat"]/li[3]/text()').extract_first().strip()
				self.item['Bua_sqft'] = re.findall('[0-9]+',sqf)[0]
			except:
				try:
					sqf = i.xpath('ul[@class="cardFeat"]/li[1]/text()').extract_first().strip()
					self.item['Bua_sqft'] = re.findall('[0-9]+',sqf)[0]
				except:
					self.item['Bua_sqft'] = '0'

			if (((not self.item['Monthly_Rent'] == '0') and (not self.item['Bua_sqft']=='0') and (not self.item['Building_name']=='None') and (not self.item['lat']=='0')) or ((not self.item['Selling_price'] == '0') and (not self.item['Bua_sqft']=='0') and (not self.item['Building_name']=='None') and (not self.item['lat']=='0')) or ((not self.item['price_per_sqft'] == '0') and (not self.item['Bua_sqft']=='0') and (not self.item['Building_name']=='None') and (not self.item['lat']=='0'))):
				self.item['quality4'] = 1
			elif (((not self.item['price_per_sqft'] == '0') and (not self.item['Building_name']=='None') and (not self.item['lat']=='0')) or ((not self.item['Selling_price'] == '0') and (not self.item['Bua_sqft']=='0') and (not self.item['lat']=='0')) or ((not self.item['Monthly_Rent'] == '0') and (not self.item['Bua_sqft']=='0') and (not self.item['lat']=='0')) or ((not self.item['Selling_price'] == '0') and (not self.item['Bua_sqft']=='0') and (not self.item['Building_name']=='None')) or ((not self.item['Monthly_Rent'] == '0') and (not self.item['Bua_sqft']=='0') and (not self.item['Building_name']=='None'))):
				self.item['quality4'] = 0.5
			else:
				self.item['quality4'] = 0
			if ((not self.item['Building_name'] == 'None') and (not self.item['listing_date'] == '0') and (not self.item['txn_type'] == 'None') and (not self.item['property_type'] == 'None') and ((not self.item['Selling_price'] == '0') or (not self.item['Monthly_Rent'] == '0'))):
				self.item['quality1'] = 1
			else:
				self.item['quality1'] = 0

			if ((not self.item['Launch_date'] == '0') or (not self.item['Possession'] == '0')):
				self.item['quality2'] = 1
			else:
				self.item['quality2'] = 0

			if ((not self.item['mobile_lister'] == 'None') or (not self.item['listing_by'] == 'None') or (not self.item['name_lister'] == 'None')):
				self.item['quality3'] = 1
			else:
				self.item['quality3'] = 0

			yield self.item

		if (not 'NO PROPERTIES FOUND IN THIS AREA' in str(response.body)):
			if self.page==1:
				nxt_url = 'http://bookmyflat.com/properties-search-results/page/{}/?sort=newest&search_city=Mumbai&search_lat&search_lng&search_category=0&search_type=0'.format(str(self.page+1))
				self.page = 2
			else:
				next_page = int(response.url.split('?')[0].split('/')[-2])
				nxt_url = 'http://bookmyflat.com/properties-search-results/page/{}/?sort=newest&search_city=Mumbai&search_lat&search_lng&search_category=0&search_type=0'.format(str(next_page+1))
			yield Request(nxt_url,callback=self.parse)
from scrapy.spiders import BaseSpider
from scrapy.http import Request
from scrapy.selector import Selector
from sulekha.items import PropertyItem
from scrapy.spiders import CrawlSpider, Rule
#from scrap_proj.items import ExtractingItem
from scrapy.linkextractors.sgml import SgmlLinkExtractor
from datetime import datetime as dt
import datetime
import re
import time

class MySpider(CrawlSpider):
	name = "SulekhaSpider"
	allowed_domains = ['property.sulekha.com']
	start_urls = ["http://property.sulekha.com/property-in-mumbai-for-sale_page-1?sortorder=recent",
	'http://property.sulekha.com/property-for-rent/mumbai/page-1?sortorder=recent'
	]
	custom_settings = {
			'DEPTH_LIMIT': 10000,
			'DOWNLOAD_DELAY': 1
		}
	
	item = PropertyItem()
	#c = ExtractingItem()
	def parse(self, response):
		hxs = Selector(response)
		
		data = hxs.xpath("//li[@class='list-box']")
		
		for i in data:
			'''
			Extracting the urls for each property and jump to new page of that property
			'''
			url = 'http://property.sulekha.com'+i.xpath('div[@class="header"]/div[@class="title"]/strong/a[@class="GAPListingTitle"]/@href').extract_first()

			yield Request(url,callback=self.parse1,dont_filter=True)

		curPage = int(response.url.split('?')[0].split('-')[-1])
		#print curPage

		if 'Next' in response.xpath('//div[@id="pagediv"]/ul/li[last()]/a/text()').extract_first():
			nextPage = response.xpath('//div[@class="pagination"]/ul/li[last()]/a/@href').extract_first()
			next_url = 'http://property.sulekha.com'+nextPage
			#print next_url
			yield Request(next_url,callback=self.parse)

	def parse1(self , response):
		hxs = Selector(response)
		#print response.body

		'''
		Assigning default values to items 
		'''
		self.item['city'] = 'mumbai'
		#self.c['city'] = 'mumbai'
		self.item['platform'] = 'Sulekha'
		self.item['carpet_area'] = '0'
		self.item['management_by_landlord'] = 'None'
		self.item['areacode'] = 'None'
		self.item['mobile_lister'] = 'None'
		self.item['google_place_id'] = 'None'
		self.item['Launch_date'] = 'None'
		self.item['Possession'] = 'None'
		self.item['config_type'] = 'None'
		self.item['Bua_sqft'] = '0'
		self.item['property_type'] = 'None'
		self.item['txn_type'] = 'None'
		self.item['Status'] = 'None'
		self.item['listing_by'] = 'None'
		self.item['age'] = 'None'
		self.item['address'] = 'None'
		self.item['price_on_req'] = 'false'
		self.item['Building_name'] = 'None'
		self.item['sublocality'] = 'None'
		self.item['price_per_sqft'] = '0'
		self.item['name_lister'] = 'None'
		self.item['Monthly_Rent'] = '0'
		self.item['Selling_price'] = '0'

		self.item['data_id'] = response.url.split('_')[-1]

		self.item['locality'] = hxs.xpath('//input[@id="d_locality"]/@value').extract_first()

		try:
			sub = hxs.xpath('//ul[@class="page-details"]/li[2]/span/text()').extract_first()
			if 'Land Mark:' in sub:
				self.item['sublocality'] = hxs.xpath('//ul[@class="page-details"]/li[2]/span[2]/text()').extract_first().strip()
		except:
			self.item['sublocality'] = 'None'

		if '-sale-' in str(response.url):
			if self.item['sublocality'] == 'None':
				sub = hxs.xpath('//div[@class="page-title"]/div[@class="pull-left"]/small/text()').extract()
				self.item['sublocality'] = sub[1].strip()
		if '-rent-' in str(response.url):
			if self.item['sublocality'] == 'None':
				sub = hxs.xpath('//div[@class="page-title"]/span/small/text()').extract()
				self.item['sublocality'] = sub[1].strip()

		self.item['lat'] = hxs.xpath('//input[@id="hdnLat"]/@value').extract_first()

		self.item['longt'] = hxs.xpath('//input[@id="hdnLong"]/@value').extract_first()

		area = hxs.xpath('//input[@id="rawUrl"]/@value').extract_first()
		ch_area = re.findall('[0-9]+',area)
		if ch_area:
			self.item['Bua_sqft'] = ch_area[0]
		else:
			self.item['Bua_sqft'] = '0'

		t_type = hxs.xpath('//input[@id="rawUrl"]/@value').extract_first()
		if '-rent-' in t_type:
			self.item['txn_type'] = 'rent'
		if '-resale-' in t_type:
			self.item['txn_type'] = 'resale'
		if '-sale-' in t_type:
			self.item['txn_type'] = 'sale'

		if 'sale' in self.item['txn_type']:
			bildg = hxs.xpath('//div[@class="pull-left"]/h1/text()').extract_first()
			if (' at ' in bildg) and (' in ' in bildg):
				self.item['Building_name'] = bildg.split(' at ')[-1].split(' in ')[0]
		if 'rent' in self.item['txn_type']:
			bildg = hxs.xpath('//div[@class="page-title"]/span/h1/text()').extract_first()
			if (' at ' in bildg) and (' in ' in bildg):
				self.item['Building_name'] = bildg.split(' at ')[-1].split(' in ')[0]

		price = hxs.xpath('//span[@class="price-green22"]/text()').extract()[-1].strip()
		if 'ale' in self.item['txn_type']:
			if 'lakhs' in price:
				price = str(float(price.split(' lakhs')[0])*100000)
				self.item['Selling_price'] = price
			elif 'crores' in price:
				price = str(float(price.split(' crores')[0])*10000000)
				self.item['Selling_price'] = price
			elif 'crore' in price:
				price = str(float(price.split(' crore')[0])*10000000)
				self.item['Selling_price'] = price
			else:
				self.item['Selling_price'] = price
		if 'rent' in self.item['txn_type']:
			if ',' in price:
				self.item['Monthly_Rent'] = price.replace(',','')
			elif 'lakhs' in price:
				price = str(float(price.split(' lakhs')[0])*100000)
				self.item['Monthly_Rent'] = price
			elif 'crores' in price:
				price = str(float(price.split(' crores')[0])*10000000)
				self.item['Monthly_Rent'] = price
			elif 'crore' in price:
				price = str(float(price.split(' crore')[0])*10000000)
				self.item['Monthly_Rent'] = price
			else:
				self.item['Monthly_Rent'] = price

		self.item['property_type'] = hxs.xpath('//input[@id="d_primarytag"]/@value').extract_first()

		if 'Commercial' in self.item['property_type']:
			poss = hxs.xpath('//div[@class="span6 push"]/ul/li[3]/span[1]/text()').extract_first()
			if 'Possession:' in poss:
				self.item['Possession'] = hxs.xpath('//div[@class="span6 push"]/ul/li[3]/span[2]/text()').extract_first()
		elif 'Apartments' in self.item['property_type']:
			poss = hxs.xpath('//div[@class="span6 push"]/ul/li[5]/span[1]/text()').extract_first()
			if 'Possession:' in poss:
				self.item['Possession'] = hxs.xpath('//div[@class="span6 push"]/ul/li[5]/span[2]/text()').extract_first()
			elif 'Property Age:' in poss:
				self.item['age'] = hxs.xpath('//div[@class="span6 push"]/ul/li[5]/span[2]/text()').extract_first()
		elif 'Plots & Land' in self.item['property_type']:
			self.item['Possession'] = 'None'

		if 'Builder' in hxs.xpath('//div[@class="page-details-info"]/i[2]/text()').extract_first():
			self.item['listing_by'] = hxs.xpath('//div[@class="page-details-info"]/text()').extract()[2]
		else:
			self.item['name_lister'] = hxs.xpath('//div[@class="page-details-info"]/text()').extract()[2]

		apa = hxs.xpath('//input[@id="hfldTitle"]/@value').extract_first()
		if ('BHK' in apa) or ('RK' in apa):
			self.item['config_type'] = apa.split('- ')[-1].split(' Apartment')[0]
			if len(self.item['config_type'])>7:
				conf = re.findall('[0-9]\sBHK',apa)+re.findall('[0-9]\sRK',apa)+re.findall('[0-9]BHK',apa)+re.findall('[0-9]RK',apa)
				if conf:
					self.item['config_type'] = conf[0]
		if self.item['config_type']=='None':
			conf = re.findall('[0-9]\sBHK',bildg)+re.findall('[0-9]\sRK',bildg)+re.findall('[0-9]BHK',bildg)+re.findall('[0-9]RK',bildg)
			if conf:
				self.item['config_type'] = conf[0]

		self.item['Details'] = hxs.xpath('//div[@id="LdHtml"]/text()').extract()[0].strip()
		
		if 'rent' in self.item['txn_type']:
			dates = hxs.xpath('//div[@class="page-title"]/span/small/text()').extract()[-1].strip().split('Posted on ')[-1]
			self.item['listing_date'] = dt.strftime(dt.strptime(dates,"%b %d, %Y"),"%m/%d/%Y %H:%M:%S")
			self.item['updated_date'] = self.item['listing_date']
		if 'sale' in self.item['txn_type']:
			dates = hxs.xpath('//div[@class="page-title"]/div[@class="pull-left"]/small/text()').extract()[-1].strip().split('Posted on  ')[-1]
			self.item['listing_date'] = dt.strftime(dt.strptime(dates,"%b %d, %Y"),"%m/%d/%Y %H:%M:%S")
			self.item['updated_date'] = self.item['listing_date']

		if ((not self.item['Building_name'] == 'None') and (not self.item['listing_date'] == 'None') and (not self.item['txn_type'] == 'None') and (not self.item['property_type'] == 'None') and ((not self.item['Selling_price'] == '0') or (not self.item['Monthly_Rent'] == '0'))):
			self.item['quality1'] = 1
		else:
			self.item['quality1'] = 0
		if ((not self.item['Launch_date'] == 'None') or (not self.item['Possession'] == 'None')):
			self.item['quality2'] = 1
		else:
			self.item['quality2'] = 0
		if ((not self.item['mobile_lister'] == 'None') or (not self.item['listing_by'] == 'None') or (not self.item['name_lister'] == 'None')):
			self.item['quality3'] = 1
		else:
			self.item['quality3'] = 0
		
		#print "++++++++++++++++++++++++++++++++++++++++++++++"
		yield self.item
		#yield self.c
		#print "++++++++++++++++++++++++++++++++++++++++++++++"
import scrapy
from scraping.items import ScrapingItem
from scrapy.spiders import Spider
from scrapy.spiders import CrawlSpider, Rule
#from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.http import Request
from scrapy.selector import Selector
#from scrapy.selector import HtmlXPathSelector
from urlparse import urljoin
import time
import datetime
import re
from datetime import datetime as dt
import pymongo
from scrapy import log


class Scraping(CrawlSpider):
	name = 'scrapeandPost'
	
	start_urls = []

	custom_settings = {
            'DEPTH_LIMIT' : 10000,
            'DOWNLOAD_DELAY': 5
        }

	item = ScrapingItem()

	def __init__(self):
		MONGODB_SERVER = "localhost"
		MONGODB_PORT = 27017
		# MONGODB_DB = "scraping"
		# MONGODB_COLLECTION = "scrape"
		connection = pymongo.MongoClient(MONGODB_SERVER,MONGODB_PORT)
		db = connection['scrapingandposting']
		self.collection = db['Andheri_1']
		self.collection_1 = db['Bandra_1']
		self.collection_s = db['Santacruz']
		self.collection_v = db['vile']

	
	def parse(self , response):
		hxs = Selector(response)

		if ('pagination' in str(response.body)):
			data = hxs.xpath('//div[contains(@id,"resultBlockWrapper")]')
			#print len(data)
			for i in data:
				if 'Andheri-West' in str(response.url):
					self.item['locality'] = 'Andheri West '
				if 'Andheri-East' in str(response.url):
					self.item['locality'] = 'Andheri East '
				if 'Bandra-West' in str(response.url):
					self.item['locality'] = 'Bandra West '
				if 'Bandra-East' in str(response.url):
					self.item['locality'] = 'Bandra East '
				if 'Santacruz-West' in str(response.url):
					self.item['locality'] = 'Santacruz West '
				if 'Santacruz-East' in str(response.url):
					self.item['locality'] = 'Santacruz East '
				if 'Vile-Parle-West' in str(response.url):
					self.item['locality'] = 'Vile parle west '
				if 'Vile-Parle-East' in str(response.url):
					self.item['locality'] = 'Vile Parle East '
				self.item['sub_loc'] = i.xpath('div[@class="srpColm2"]/div[@class="minHeightBlock"]/div[@class="proColmleft"]/div[@class="proNameWrap "]/div[@class="proNameColm1"]/div[@class="srpTopDetailWrapper"]/div[@class="srpAnchor"]/p/a/span[@class="maxProDesWrap showNonCurtailed"]/span[@class="localityFirst"]/text()').extract_first()

				self.item['bed'] = i.xpath('div[@class="srpColm2"]/div[@class="minHeightBlock"]/div[@class="proColmleft"]/div[@class="proNameWrap "]/div[@class="proNameColm1"]/div[@class="srpTopDetailWrapper"]/div[@class="srpAnchor"]/p/a/input[contains(@id,"bedroomVal")]/@value').extract_first()

				try:
					self.item['sqft'] = i.xpath('div[@class="srpColm2"]/div[@class="minHeightBlock"]/div[@class="proColmleft"]/div[@class="proDetailsRow proDetailsRowListing proDetailsRowRent"]/div[1]/ul/input/@value').extract_first().split(' ')[0]
				except:
					if '1' in self.item['bed']:
						self.item['sqft'] = '600'
					if '2' in self.item['bed']:
						self.item['sqft'] = '800'
					if '3' in self.item['bed']:
						self.item['sqft'] = '1100'
					if '4' in self.item['bed']:
						self.item['sqft'] = '1500'

				self.item['status'] = i.xpath('input[contains(@id,"furnshingStatus")]/@value').extract_first()
				#bprices=float(re.sub("\D", "",bprices))
				self.item['flr'] = i.xpath('input[contains(@id,"floorNo")]/@value').extract_first()
				print self.item['flr']
				if 'Ground' in self.item['flr']:
					self.item['flr'] = '0'
				else:
					self.item['flr'] = str(re.sub("\D","",self.item['flr']))
				if self.item['flr'] == '':
					self.item['flr'] = '0'

				self.item['bath'] = i.xpath('input[contains(@id,"bathroom")]/@value').extract_first()

				try:
					price = i.xpath('div[@class="srpColm2"]/div[@class="minHeightBlock"]/div[@class="proColmleft"]/div[@class="proNameWrap "]/div[@class="proNameColm1"]/div[@class="srpTopDetailWrapper"]/div[@class="srpPriceWrap newPriceBlock"]/div[@class="proPriceColm2"]/div[@class="proPrice"]/span[@class="proPriceField"]/text()').extract_first()
					if 'Lac' in price:
						price = str(float(price.split(' Lac')[0])*100000)
						self.item['rent_price'] = price
					elif 'Cr' in price:
						price = str(float(price.split(' Cr')[0])*10000000)
						self.item['rent_price'] = price
					else:
						price = price.replace(',','')
						self.item['rent_price'] = price

				except:
					if (('1' in self.item['bed']) and ('Andheri' in str(response.url))):
						self.item['rent_price'] = '40000'
					if (('2' in self.item['bed']) and ('Andheri' in str(response.url))):
						self.item['rent_price'] = '50000'
					if (('3' in self.item['bed']) and ('Andheri' in str(response.url))):
						self.item['rent_price'] = '70000'
					if (('4' in self.item['bed']) and ('Andheri' in str(response.url))):
						self.item['rent_price'] = '140000'
					if (('1' in self.item['bed']) and ('Bandra' in str(response.url))):
						self.item['rent_price'] = '50000'
					if (('2' in self.item['bed']) and ('Bandra' in str(response.url))):
						self.item['rent_price'] = '70000'
					if (('3' in self.item['bed']) and ('Bandra' in str(response.url))):
						self.item['rent_price'] = '120000'
					if (('4' in self.item['bed']) and ('Bandra' in str(response.url))):
						self.item['rent_price'] = '250000'
					if (('1' in self.item['bed']) and ('Santacruz' in str(response.url))):
						self.item['rent_price'] = '50000'
					if (('2' in self.item['bed']) and ('Santacruz' in str(response.url))):
						self.item['rent_price'] = '80000'
					if (('3' in self.item['bed']) and ('Santacruz' in str(response.url))):
						self.item['rent_price'] = '120000'
					if (('4' in self.item['bed']) and ('Santacruz' in str(response.url))):
						self.item['rent_price'] = '250000'
					if (('1' in self.item['bed']) and ('Vile' in str(response.url))):
						self.item['rent_price'] = '50000'
					if (('2' in self.item['bed']) and ('Vile' in str(response.url))):
						self.item['rent_price'] = '80000'
					if (('3' in self.item['bed']) and ('Vile' in str(response.url))):
						self.item['rent_price'] = '120000'
					if (('4' in self.item['bed']) and ('Vile' in str(response.url))):
						self.item['rent_price'] = '250000'


				self.item['depo'] = str(float(self.item['rent_price'])*3)

				try:
					self.item['t_flr'] = i.xpath('div[@class="srpColm2"]/div[@class="minHeightBlock"]/div[@class="proColmleft"]/div[@class="proDetailsRow proDetailsRowListing proDetailsRowRent"]/div[1]/ul/li[3]/text()').extract_first().split('(of ')[-1].replace(')','')
				except:
					self.item['t_flr'] = str(int(self.item['flr'])+3)

				if self.item['sub_loc'] in self.item['locality']:
					self.item['title'] = 'A sapcious '+self.item['bed']+' BHK in '+self.item['locality']+' for rent'
				else:
					self.item['title'] = 'A sapcious '+self.item['bed']+' BHK in '+self.item['sub_loc']+','+self.item['locality']+' for rent'


				self.item['detail'] = self.item['bed']+' BHK '+'Flat is immediately availbale and location is '+self.item['locality']+' with all modern amenities for more detail call us...'

				yield self.item
				if 'Andheri' in str(response.url):
					self.collection.insert(dict(self.item))
					print "++++++++++++++++++++++++++++++++"
					log.msg("Andheri Data added to Andheri database!",level=log.DEBUG)
				if 'Bandra' in str(response.url):
					self.collection_1.insert(dict(self.item))
					print "--------------------------------"
					log.msg("Bandra Data added to Bandra database!",level=log.DEBUG)
				if 'Santacruz' in str(response.url):
					self.collection_s.insert(dict(self.item))
					print ">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>"
					log.msg("Santacruz Data added to Santacruz database!",level=log.DEBUG)
				if 'Vile' in str(response.url):
					self.collection_v.insert(dict(self.item))
					print "<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<"
					log.msg("Vile Data added to Vile database!",level=log.DEBUG)

		'''if 'Andheri-West' in str(response.url):
			cur = int(response.url.split('-')[-1])
			next = response.xpath('//div[@id="pagination"]/span/a[last()]/@href').extract_first()
			print next
			if ((not next==None) and (not 'javascript:void(0)' in next)):
				next_page = next.split('-')[-1]
				next_url = 'http://www.magicbricks.com/property-for-rent/residential-real-estate?bedroom=2,3,4&proptype=Multistorey-Apartment,Builder-Floor-Apartment,Penthouse,Studio-Apartment,Service-Apartment,Residential-House,Villa&Locality=Andheri-West&cityName=Mumbai&BudgetMin=50000/Page-{}'.format(str(next_page))
				yield Request(next_url,callback=self.parse)
			elif ('pagination' in str(response.body)):
				next_url = 'http://www.magicbricks.com/property-for-rent/residential-real-estate?bedroom=2,3,4&proptype=Multistorey-Apartment,Builder-Floor-Apartment,Penthouse,Studio-Apartment,Service-Apartment,Residential-House,Villa&Locality=Andheri-West&cityName=Mumbai&BudgetMin=50000/Page-{}'.format(str(cur+1))
				yield Request(next_url,callback=self.parse)
		if 'Andheri-East' in str(response.url):
			cur = int(response.url.split('-')[-1])
			next = response.xpath('//div[@id="pagination"]/span/a[last()]/@href').extract_first()
			print next
			if ((not next==None) and (not 'javascript:void(0)' in next)):
				next_page = next.split('-')[-1]
				next_url = 'http://www.magicbricks.com/property-for-rent/residential-real-estate?bedroom=2,3,4&proptype=Multistorey-Apartment,Builder-Floor-Apartment,Penthouse,Studio-Apartment,Service-Apartment,Residential-House,Villa&Locality=Andheri-East&cityName=Mumbai&BudgetMin=50000/Page-{}'.format(str(next_page))
				yield Request(next_url,callback=self.parse)
			elif ('pagination' in str(response.body)):
				next_url = 'http://www.magicbricks.com/property-for-rent/residential-real-estate?bedroom=2,3,4&proptype=Multistorey-Apartment,Builder-Floor-Apartment,Penthouse,Studio-Apartment,Service-Apartment,Residential-House,Villa&Locality=Andheri-East&cityName=Mumbai&BudgetMin=50000/Page-{}'.format(str(cur+1))
				yield Request(next_url,callback=self.parse)
		if 'Bandra-West' in str(response.url):
			cur = int(response.url.split('-')[-1])
			next = response.xpath('//div[@id="pagination"]/span/a[last()]/@href').extract_first()
			print next
			if ((not next==None) and (not 'javascript:void(0)' in next)):
				next_page = next.split('-')[-1]
				next_url = 'http://www.magicbricks.com/property-for-rent/residential-real-estate?bedroom=2,3,4&proptype=Multistorey-Apartment,Builder-Floor-Apartment,Penthouse,Studio-Apartment,Service-Apartment,Residential-House,Villa&Locality=Bandra-West&cityName=Mumbai&BudgetMin=70000/Page-{}'.format(str(next_page))
				yield Request(next_url,callback=self.parse)
			elif ('pagination' in str(response.body)):
				next_url = 'http://www.magicbricks.com/property-for-rent/residential-real-estate?bedroom=2,3,4&proptype=Multistorey-Apartment,Builder-Floor-Apartment,Penthouse,Studio-Apartment,Service-Apartment,Residential-House,Villa&Locality=Bandra-West&cityName=Mumbai&BudgetMin=70000/Page-{}'.format(str(cur+1))
				yield Request(next_url,callback=self.parse)
		if 'Bandra-East' in str(response.url):
			cur = int(response.url.split('-')[-1])
			next = response.xpath('//div[@id="pagination"]/span/a[last()]/@href').extract_first()
			print next
			if ((not next==None) and (not 'javascript:void(0)' in next)):
				next_page = next.split('-')[-1]
				next_url = 'http://www.magicbricks.com/property-for-rent/residential-real-estate?bedroom=2,3,4&proptype=Multistorey-Apartment,Builder-Floor-Apartment,Penthouse,Studio-Apartment,Service-Apartment,Residential-House,Villa&Locality=Bandra-East&cityName=Mumbai&BudgetMin=70000/Page-{}'.format(str(next_page))
				yield Request(next_url,callback=self.parse)
			elif ('pagination' in str(response.body)):
				next_url = 'http://www.magicbricks.com/property-for-rent/residential-real-estate?bedroom=2,3,4&proptype=Multistorey-Apartment,Builder-Floor-Apartment,Penthouse,Studio-Apartment,Service-Apartment,Residential-House,Villa&Locality=Bandra-East&cityName=Mumbai&BudgetMin=70000/Page-{}'.format(str(cur+1))
				yield Request(next_url,callback=self.parse)'''
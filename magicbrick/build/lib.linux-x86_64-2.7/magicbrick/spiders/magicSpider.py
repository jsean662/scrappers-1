import scrapy
import logging
from magicbrick.items import MagicbrickItem
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
import sys
import re

class MagicSpider(scrapy.Spider):
	name = 'magicSpider'
	allowed_domains = ['magicbricks.com']
	start_urls = ['http://www.magicbricks.com/property-for-sale/residential-real-estate?proptype=Multistorey-Apartment,Builder-Floor-Apartment,Penthouse,Studio-Apartment,Residential-House,Villa&cityName=Mumbai/Page-1']
	#http://www.magicbricks.com/property-for-sale/residential-real-estate?proptype=Multistorey-Apartment,Builder-Floor-Apartment,Penthouse,Studio-Apartment,Residential-House,Villa&cityName=Navi-Mumbai/Page-1
	custom_settings = {
			'DEPTH_LIMIT' : 10000,
			'DOWNLOAD_DELAY': 5
		}   
	  
	def parse(self,response):
			hxs = Selector(response)

			data = hxs.xpath('//div[contains(@id,"resultBlockWrapper")]')
	
			for i in data:
				item = MagicbrickItem()
		
				item['name_lister'] = 'None'
				item['Details'] = 'None'
				item['listing_by'] = 'None'
				item['address'] = 'None'
				item['sublocality'] = 'None'
				item['age'] = 'None'
				item['google_place_id'] = 'None'
				item['lat'] = 0
				item['longt'] = 0
				item['Possession'] = 'None'
				item['Launch_date'] = 'None'
				item['mobile_lister'] = 'None'
				item['areacode'] = 'None'
				item['management_by_landlord'] = 'None'

				item['Building_name'] = i.xpath('div/input[contains(@id,"projectName")]/@value').extract_first()
				if item['Building_name']=='':
					item['Building_name'] = 'None'

				try:
					item['lat'] = i.xpath('div/div[@class="srpColm2"]/div[@class="proColmleft"]/div[@class="proNameWrap proNameWrapBuy"]/div[@class="proNameColm1"]/span[@class="seeOnMapLink seeOnMapLinkBuy"]/span[@class="stopParentLink"]/@onclick').extract_first().split('&')[0].split('?')[-1].split("=")[-1]
					if item['lat'] == '':
						item['lat'] = '0'
				except:
					item['lat'] = '0'
			
				try:
					item['longt'] = i.xpath('div/div[@class="srpColm2"]/div[@class="proColmleft"]/div[@class="proNameWrap proNameWrapBuy"]/div[@class="proNameColm1"]/span[@class="seeOnMapLink seeOnMapLinkBuy"]/span[@class="stopParentLink"]/@onclick').extract_first().split('&')[1].split("=")[-1]
					if item['longt'] == '':
						item['longt'] = '0'
				except:
					item['longt'] = '0'

				item['platform'] = 'magicbricks'
				item['carpet_area'] = '0'
			
				ids = i.xpath('@id').extract_first()
				item['data_id'] = re.findall('[0-9]+',ids)[0]
			
				try:
					item['config_type'] = i.xpath('div/div[@class="srpColm2"]/div[@class="proColmleft"]/div[1]/div/p/a/input[contains(@id,"bedroomVal")]/@value').extract_first()+'BHK'
					if item['config_type'] == 'BHK':
						if 'Studio' in i.xpath('div/div[@class="srpColm2"]/div[@class="proColmleft"]/div[1]/div/p/a/input[contains(@id,"propertyVal")]/@value').extract_first():
							item['config_type'] = 'Studio'
				except:
					item['config_type'] = 'None'
			
				sqf = i.xpath('div/div[@class="srpColm2"]/div[@class="proColmleft"]/div[1]/div/p/a/input[contains(@id,"propertyArea")]/@value').extract_first()
				item['Bua_sqft'] = re.findall('[0-9]+',sqf)[0]
			
				item['city'] = 'Mumbai'
			
				item['locality'] = i.xpath('div/div[@class="srpColm2"]/div[@class="proColmleft"]/div[1]/div/p/a/abbr/span[1]/span/text()').extract_first()
			
				stat = i.xpath('div/div[@class="srpColm2"]/div[@class="proColmleft"]/div[@class="proDetailsRow "]/div[@class="proDetailsRowElm"]/text()').extract()
				item['Status'] = ''.join(stat)
			
				price = i.xpath('div/div[@class="srpColm2"]/div[@class="proColmRight"]/div/div/div/span/text()').extract_first()
				if not price==None:
					if 'Lac' in price:
						item['Selling_price']=str(float(price.split()[0])*100000)
					elif 'Cr' in price:
						item['Selling_price']=str(float(price.split()[0])*10000000)
					else:
						item['Selling_price'] = '0'
					if item['Selling_price'] == 'None':
						item['Selling_price'] = '0'
					item['Monthly_Rent'] = '0'
				else:
					item['Selling_price'] = '0'
					item['Monthly_Rent'] = '0'
				if item['Selling_price'] == '0' and item['Monthly_Rent'] == '0':
					item['price_on_req'] = 'true'
				else:
					item['price_on_req'] = 'false'

				try:
					sqft_per = i.xpath('div/div[@class="srpColm2"]/div[@class="proColmRight"]/div[@class="proPriceColm2"]/div[@class="proPriceColm2"]/div[@class="sqrPrice"]/span[@class="sqrPriceField"]/text()').extract_first()
					if (not sqft_per==None):
						item['price_per_sqft'] = ''.join(re.findall('[0-9]+',sqft_per))
				except:
					item['price_per_sqft'] = '0'
			
				try:
					item['name_lister'] = i.xpath('div/div[@class="srpColm2"]/div[@class="proColmleft"]/div[@class="proDetailsRow "]/input[contains(@id,"devName")]/@value').extract_first()
					if item['name_lister']=='':
						item['name_lister'] = 'None'
				except:
					item['name_lister'] = 'None'
			
				item['property_type'] = 'Residential'

				item['txn_type'] = i.xpath('div/input[contains(@id,"transactionType")]/@value').extract_first()

				day = i.xpath('div/input[contains(@id,"createDate")]/@value').extract_first()
		
				item['listing_date'] = dt.strftime(dt.strptime(day,"%b %d, '%y"),'%m/%d/%Y %H:%M:%S')
			
				item['updated_date'] = item['listing_date']
			
				if ((not item['Building_name'] == 'None') and (not item['listing_date'] == 'None') and (not item['txn_type'] == 'None') and (not item['property_type'] == 'None') and ((not item['Selling_price'] == '0') or (not item['Monthly_Rent'] == '0'))):
					item['quality1'] = 1
				else:
					item['quality1'] = 0
		
				if ((not item['Launch_date'] == 'None') and (not item['Possession'] == 'None')):
					item['quality2'] = 1
				else:
					item['quality2'] = 0

				if ((not item['mobile_lister'] == 'None') or (not item['listing_by'] == 'None') or (not item['name_lister'] == 'None')):
					item['quality3'] = 1
				else:
					item['quality3'] = 0
				yield item

			cur = int(response.url.split('-')[-1])
			# next = response.xpath('//div[@id="pagination"]/span/a[last()]/@href').extract_first()
			# print next
			# if ((not next==None) and (not 'javascript:void(0)' in next)):
			# 	next_page = next.split('-')[-1]
			# 	next_url = '-'.join(response.url.split('-')[:-1])+'-'+str(next_page)
			# 	print next_url
			# 	yield Request(next_url,callback=self.parse)
			# elif ('pagination' in str(response.body)):
			# 	next_url = '-'.join(response.url.split('-')[:-1])+'-'+str(cur+1)
			# 	print next_url
			# 	yield Request(next_url,callback=self.parse)
			if not 'noResultContainer' in str(response.body):
				next_url = '-'.join(response.url.split('-')[:-1])+'-'+str(cur+1)
				yield Request(next_url,callback=self.parse)
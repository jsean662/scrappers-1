import scrapy
import sys
import logging
from magicbricksrent.items import MagicbricksrentItem
from scrapy.spiders import Spider
from scrapy.spiders import CrawlSpider, Rule
from scrapy.selector import Selector
from scrapy.http import Request
from scrapy.http import FormRequest
from urlparse import urljoin
from datetime import datetime as dt
from datetime import time,timedelta
from datetime import date
import time
import re

class MagicrentSpider(scrapy.Spider):
	name = 'magicbricksrentThane'
	
	allowed_domains = ['magicbricks.com']
	start_urls = ['http://www.magicbricks.com/property-for-rent/residential-real-estate?proptype=Multistorey-Apartment,Builder-Floor-Apartment,Penthouse,Studio-Apartment,Service-Apartment,Residential-House,Villa&cityName=Thane/Page-1']
	custom_settings = {
			'DEPTH_LIMIT' : 10000,
			'DOWNLOAD_DELAY': 5
		}

	def parse(self,response):
			hxs = Selector(response)
			data = hxs.xpath('//div[contains(@id,"resultBlockWrapper")]')
		
			for i in data:
				item = MagicbricksrentItem()
			
				item['platform'] = 'Magicbrick'
				item['city'] = 'Thane'
				
				item['data_id'] = i.xpath('@id').extract_first()
				item['data_id'] = re.findall('[0-9]+',item['data_id'])[0]
				
				item['txn_type'] = i.xpath('.//input[contains(@id,"transactionType")]/@value').extract_first()

				item['property_type'] = i.xpath('.//input[contains(@id,"propertyVal")]/@value').extract_first()

				try:
					item['lat'] = i.xpath('.//span[@class="seeOnMapLink seeOnMapLinkRent"]/a/@onclick').extract_first().split('&')[0].split("?")[-1].split("=")[-1]
				except:
					item['lat'] = '0'
				if item['lat'] == '':
					item['lat'] = '0'
				
				try:
					item['longt'] = i.xpath('.//span[@class="seeOnMapLink seeOnMapLinkRent"]/a/@onclick').extract_first().split('&')[1].split("=")[-1]
				except:
					item['longt'] = '0'
				if item['longt'] == '':
					item['longt'] = '0'
				
				item['locality'] = i.xpath('.//span[@class="localityFirst"]/text()').extract_first()
				
				item['Building_name'] = i.xpath('.//input[contains(@id,"projectName")]/@value').extract_first()
				if item['Building_name'] == '':
					item['Building_name'] = 'None'
				
				item['config_type'] = i.xpath('.//input[contains(@id,"bedroomVal")]/@value').extract_first()+'BHK'
				if item['config_type']=='BHK':
					item['config_type'] = '1RK'
				
				item['Selling_price'] = '0'
				
				price = i.xpath('.//span[@class="proPriceField"]/text()').extract_first()
				if price==None:
					item['Monthly_Rent'] = '0'
					item['price_on_req'] = 'true'
				elif 'Price' in price:
					item['Monthly_Rent'] = '0'
					item['price_on_req'] = 'true'
				elif 'Lac' in price:
					price = float(price.replace("Lac",""))*100000
					item['Monthly_Rent'] = str(price)
				elif 'Cr' in price:
					price = float(price.replace(" Cr",""))*10000000
					item['Monthly_Rent'] = str(price)
				else:
					price = price.replace(",","")
					item['Monthly_Rent'] = str(float(price))
				
				if item['Selling_price'] == '0' and item['Monthly_Rent'] == '0':
					item['price_on_req'] = 'true'
				else:
					item['price_on_req'] = 'false'
				
				item['price_per_sqft'] = '0'
				item['carpet_area'] = '0'
				item['address'] = 'None'
				item['sublocality'] = 'None'
				item['age'] = 'None'
				item['google_place_id'] = 'None'
				item['Launch_date'] = '0'
				item['Possession'] = '0'
				item['mobile_lister'] = 'None'
				item['areacode'] = 'None'
				item['management_by_landlord'] = 'None'
				
				item['listing_by'] = i.xpath('.//input[contains(@id,"userType")]/@value').extract_first()
				
				item['name_lister'] = i.xpath('.//input[contains(@id,"devName")]/@value').extract_first().replace('\n','')
				if item['name_lister'] == "":
					item['name_lister'] = i.xpath('.//div[@class="comNameElip"]/text()').extract_first().replace('\n','')
					if item['name_lister'] == '':
						item['name_lister'] = 'None'
				
				sq = i.xpath('.//input[contains(@id,"propertyArea")]/@value').extract_first()
				try:
					item['Bua_sqft'] = sq.split()[0]
				except:
					item['Bua_sqft'] = '0'
				
				item['Status'] = i.xpath('.//input[contains(@id,"furnshingStatus")]/@value').extract_first()
				
				item['Details'] = i.xpath('.//div[@class="proDetailsRowElm"]/ul/li/text()').extract()
				item['Details'] = ''.join(item['Details'])
				item['Details'] = item['Details'].replace('\n','')
				
				day = i.xpath('.//input[contains(@id,"createDate")]/@value').extract_first()
				
				item['listing_date'] = dt.strftime(dt.strptime(day,"%b %d, '%y"),'%m/%d/%Y %H:%M:%S')

				item['updated_date'] = item['listing_date']

				item['scraped_time'] = dt.now().strftime('%m/%d/%Y %H:%M:%S')

				if (((not item['Monthly_Rent'] == '0') and (not item['Bua_sqft']=='0') and (not item['Building_name']=='None') and (not item['lat']=='0')) or ((not item['Selling_price'] == '0') and (not item['Bua_sqft']=='0') and (not item['Building_name']=='None') and (not item['lat']=='0')) or ((not item['price_per_sqft'] == '0') and (not item['Bua_sqft']=='0') and (not item['Building_name']=='None') and (not item['lat']=='0'))):
					item['quality4'] = 1
				elif (((not item['price_per_sqft'] == '0') and (not item['Building_name']=='None') and (not item['lat']=='0')) or ((not item['Selling_price'] == '0') and (not item['Bua_sqft']=='0') and (not item['lat']=='0')) or ((not item['Monthly_Rent'] == '0') and (not item['Bua_sqft']=='0') and (not item['lat']=='0')) or ((not item['Selling_price'] == '0') and (not item['Bua_sqft']=='0') and (not item['Building_name']=='None')) or ((not item['Monthly_Rent'] == '0') and (not item['Bua_sqft']=='0') and (not item['Building_name']=='None'))):
					item['quality4'] = 0.5
				else:
					item['quality4'] = 0
				if ((not item['Building_name'] == 'None') and (not item['listing_date'] == '0') and (not item['txn_type'] == 'None') and (not item['property_type'] == 'None') and ((not item['Selling_price'] == '0') or (not item['Monthly_Rent'] == '0'))):
					item['quality1'] = 1
				else:
					item['quality1'] = 0
			
				if ((not item['Launch_date'] == '0') and (not item['Possession'] == '0')):
					item['quality2'] = 1
				else:
					item['quality2'] = 0

				if ((not item['mobile_lister'] == 'None') or (not item['listing_by'] == 'None') or (not item['name_lister'] == 'None')):
					item['quality3'] = 1
				else:
					item['quality3'] = 0
				yield item

			cur = int(response.url.split('-')[-1])

			if not 'noSearchResultPageDiv' in str(response.body):
				next_url = '-'.join(response.url.split('-')[:-1])+'-'+str(cur+1)
				yield Request(next_url,callback=self.parse)
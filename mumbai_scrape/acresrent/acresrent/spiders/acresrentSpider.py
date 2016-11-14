import scrapy
import logging
from acresrent.items import AcresrentItem
from scrapy.spiders import Spider
from scrapy.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.http import Request
from scrapy.selector import Selector
from scrapy.selector import HtmlXPathSelector
from urlparse import urljoin
import time
import datetime
from datetime import datetime as dt
import re

class AcresrentSpider(CrawlSpider):
	name = "acresrentSpider"
	allowed_domains = ['99acres.com']

	start_urls = ['http://www.99acres.com/rent-property-in-mumbai-ffid-page-1?orig_property_type=1,4,2,90,22&search_type=QS&search_location=CP12&lstacn=SEARCH&pageid=QS&src=PAGING&lastAcn=SEARCH&property_type=1,4,2,90,22'
			]
	custom_settings = {
			'DEPTH_LIMIT': 10000,
			'DOWNLOAD_DELAY': 5
		}
	#data_list = []
	def parse(self,response):
		hxs = Selector(response)
		path1 = "//div[@id='ysf']/h1"
		x1 = hxs.xpath(path1)
		path = "//div[@id='results']/div[1]/div[contains(@class,'srpWrap')]"
		x = hxs.xpath(path)
		
		ttl_itm = hxs.xpath('//input[@id="prop_count"]/@value').extract_first()
		# print ttl_itm
		
		for i in x:
			item = AcresrentItem()
			#self.data_list.append(data_id)
			data_id = i.xpath("@data-propid").extract_first()
			sqft_check = i.xpath(".//div[@class='srpDataWrap']/span[1]/b[1]/text()").extract_first()
			sqft_check = re.findall('[0-9]+',sqft_check)
			
			for s in sqft_check:
				'''
				Assign Default values
				'''
				item['Possession'] = '0'
				item['txn_type'] = 'None'
				item['Selling_price'] = '0'
				item['config_type'] = 'None'
				item['Status'] = 'None'
				item['age'] = 'None'
				item['lat'] = '0'
				item['longt'] = '0'
				item['address'] = 'None'
				item['sublocality'] = 'None'
				item['google_place_id'] = 'None'
				item['Launch_date'] = '0'
				item['mobile_lister'] = 'None'
				item['areacode'] = 'None'
				item['management_by_landlord'] = 'None'
				item['carpet_area'] = '0'

				item['data_id'] = data_id
				
				item['platform'] = '99acres'
				
				item['property_type'] = str(i.xpath('.//meta[@itemprop="name"]/@content').extract_first()).replace('for rent','')
				
				item['city'] = x1.xpath("span[3]/b/text()").extract_first().split(" ")[0]
			
				item['Bua_sqft'] =  s
				
				try:
					item['price_per_sqft'] = i.xpath(".//div[@class='srpDataWrap']/span/text()").extract()
					item['price_per_sqft'] = ''.join(item['price_per_sqft'])
					item['price_per_sqft'] = re.findall('[0-9]+',item['price_per_sqft'])
					if item['price_per_sqft']:
						item['price_per_sqft'] = item['price_per_sqft'][0]
					if not item['price_per_sqft']:
						item['price_per_sqft'] = '0'
				except:
					item['price_per_sqft'] = '0'                       
				
				try:
					item['Building_name'] = str(i.xpath(".//a[@class='sName']/b/text()").extract_first()).strip()
				except:
					try:
						item['Building_name'] = str(i.xpath(".//div[@class='srpDataWrap']/span[2]/b/text()").extract_first()).strip()
					except:
						item['Building_name'] = 'None'
				if item['Building_name'] == '':
					item['Building_name'] = 'None'


				stat1 = i.xpath("div[@class='srpDetail']/div[@class='srpDataWrap']/span[3]/span/text()").extract()
				stat2 = i.xpath("div[@class='srpDetail']/div[@class='srpDataWrap']/span[2]/span/text()").extract()

				try:
					if stat1:
						item['txn_type'] = stat1[1].encode('ascii', 'ignore').decode('ascii').replace('On ','')
						if 'ent' in item['txn_type']:
							item['Status'] = stat1[5].strip()
							item['age'] = stat1[3].strip()
				except:
					pass

				try:
					if stat2:
						item['txn_type'] = stat2[1].encode('ascii', 'ignore').decode('ascii').replace('On ','')
						if 'ent' in item['txn_type']:
							item['Status'] = stat2[5].strip()
							item['age'] = stat2[3].strip()
				except:
					pass
				
				detail1 = i.xpath("div[@class='srpDetail']/div[@class='srpDataWrap']/div[4]/b/text()").extract_first()
				if (not detail1==None) and ('Description :' in detail1):
					item['Details'] = i.xpath("div[@class='srpDetail']/div[@class='srpDataWrap']/div[4]/text()").extract()[-1].strip()
				else:
					detail2 = i.xpath("div[@class='srpDetail']/div[@class='srpDataWrap']/div[3]/b/text()").extract_first()
					if (not detail2==None) and ('Description :' in detail2):
						item['Details'] = i.xpath("div[@class='srpDetail']/div[@class='srpDataWrap']/div[3]/text()").extract()[-1].strip()
					else:
						item['Details'] = 'None'
				
				if 'Studio Apartment' in item['property_type']:
					item['config_type'] = '1RK'
				else:
					con1 = i.xpath("div[@class='wrapttl']/div[1]/a/text()").extract_first()
					conf = re.findall('[0-9]',con1)[0]
					item['config_type'] = conf+'BHK'
				
				item['locality'] = i.xpath('.//meta[@itemprop="addressLocality"]/@content').extract_first()
				
				try:
					build = i.xpath("div[@class='srpDetail']/div[last()]/text()").extract()[0].encode('ascii', 'ignore').decode('ascii')
					if 'Builder' in build:
						item['listing_by'] = 'Builder'
						item['name_lister'] = build.split(' Posted')[0].split(':')[-1].strip()
					elif 'Owner' in build:
						item['listing_by'] = 'Owner'
						item['name_lister'] = build.split(' Posted')[0].split(':')[-1].strip()
					else:
						item['listing_by'] = 'None'
						item['name_lister'] = 'None'
				except:
					item['listing_by'] = 'None'
					item['name_lister'] = 'None'

				try:
					date_string = str(i.xpath("div[@class='srpDetail']/div[last()]/text()").extract()).split(':')[-1].replace(' ','').replace(']','').replace('\\n','').replace("'","")
					if date_string == 'Today':
						date = time.strftime('%b%d,%Y')
					else:
						if date_string == 'Yesterday':
							date = dt.strftime(dt.now()-datetime.timedelta(1),'%b%d,%Y')
						else:
							date = date_string.replace('"','')
					date = dt.strftime(dt.strptime(date,'%b%d,%Y'),'%m/%d/%Y %H:%M:%S')
					item['listing_date'] = date
					item['updated_date'] = item['listing_date']
				except:
					logging.log(logging.ERROR,date)
					item['listing_date'] = dt.now().strftime('%m/%d/%Y %H:%M:%S')
					item['updated_date'] = item['listing_date']
				
				price = i.xpath('.//b[@itemprop="price"]/text()').extract_first()
				# print price
				if price:
					if 'Lac' in price:
						price = str(float(str(price.split()[0])) * 100000)
						item['Monthly_Rent'] = price
					elif 'Crore' in price:
						price =  str(float(str(price.split()[0])) * 10000000)
						item['Monthly_Rent'] = price
					else:						
						item['Monthly_Rent'] = price.replace(',','')
						item['Selling_price'] = '0'
				else:
					item['Selling_price'] = '0'
					item['Monthly_Rent'] = '0'
				if 'Request' in item['Monthly_Rent']:
					item['Selling_price'] = '0'
					item['Monthly_Rent'] = '0'
				
				if item['Monthly_Rent'] == '0' and item['Selling_price'] == '0':
					item['price_on_req'] = 'true'
				else:
					item['price_on_req'] = 'false'
				
				lat_lng = str(i.xpath("div[@class='wrapttl']/i/@data-maplatlngzm").extract_first()).split(',')
				item['lat'] = lat_lng[0]
				if len(lat_lng)>1:
					item['longt'] = lat_lng[1]
				else:
					item['longt'] = '0'
				if (('None' in lat_lng) or lat_lng==None):
					item['lat'] = '0'
					item['longt'] = '0'
								
				if (((not item['Monthly_Rent'] == '0') and (not item['Bua_sqft']=='0') and (not item['Building_name']=='None') and (not item['lat']=='0')) or ((not item['Selling_price'] == '0') and (not item['Bua_sqft']=='0') and (not item['Building_name']=='None') and (not item['lat']=='0')) or ((not item['price_per_sqft'] == '0') and (not item['Bua_sqft']=='0') and (not item['Building_name']=='None') and (not item['lat']=='0'))):
					item['quality4'] = 1
				elif (((not item['price_per_sqft'] == '0') and (not item['Building_name']=='None') and (not item['lat']=='0')) or ((not item['Selling_price'] == '0') and (not item['Bua_sqft']=='0') and (not item['lat']=='0')) or ((not item['Monthly_Rent'] == '0') and (not item['Bua_sqft']=='0') and (not item['lat']=='0'))):
					item['quality4'] = 0.5
				else:
					item['quality4'] = 0
				if ((not item['Building_name'] == 'None') and (not item['listing_date'] == '0') and (not item['txn_type'] == 'None') and (not item['property_type'] == 'None') and ((not item['Selling_price'] == '0') or (not item['Monthly_Rent'] == '0'))):
					item['quality1'] = 1
				else:
					item['quality1'] = 0
	
				if ((not item['Launch_date'] == '0') or (not item['Possession'] == '0')):
					item['quality2'] = 1
				else:
					item['quality2'] = 0

				if ((not item['mobile_lister'] == 'None') or (not item['listing_by'] == 'None') or (not item['name_lister'] == 'None')):
					item['quality3'] = 1
				else:
					item['quality3'] = 0
				yield item
				
		#print response.body
		next_page = response.xpath('//input[@id="button_next"]/@value').extract_first()
		if next_page==None and next_page <= (ttl_itm/30):
			next_page = int(response.url.split('?')[0].split('-')[-1])+1
		next_url = 'http://www.99acres.com/rent-property-in-mumbai-ffid-page-{}?orig_property_type=1,4,2,90,22&search_type=QS&search_location=CP12&lstacn=SEARCH&pageid=QS&src=PAGING&lastAcn=SEARCH&property_type=1,4,2,90,22'.format(str(next_page))
		yield Request(next_url,callback=self.parse)
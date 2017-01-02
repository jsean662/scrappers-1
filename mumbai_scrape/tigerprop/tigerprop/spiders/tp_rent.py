import scrapy
from tigerprop.items import TigerpropItem
from scrapy.spiders import Spider
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.selector import Selector
from scrapy.selector import HtmlXPathSelector
from scrapy.http import Request
import json
from scrapy.selector import XmlXPathSelector
import lxml.etree as etree
from urlparse import urljoin
import urllib
import time
from datetime import datetime as dt

class PropRentSpider(Spider):
	name = "proptigerresaleMumbai"
	start_urls = ['https://www.proptiger.com/data/v2/entity/resale-listing?selector={%22filters%22:{%22and%22:[{%22equal%22:{%22bookingStatusId%22:1}},{%22equal%22:{%22cityId%22:18}}]},%22paging%22:{%22start%22:0,%22rows%22:15}}']
	allowed_domains = ["www.proptiger.com"]
	rules = (Rule(LinkExtractor(deny=(), allow=('http://www.proptiger.com/'), ), callback='parse', follow=True, ),)
	custom_settings = {
	        'DEPTH_LIMIT': 10000,
	        'DOWNLOAD_DELAY': 2
	    }

	def parse(self, response):
		jr = response.body
		jd = json.loads(jr)
		handle_http_list = [500]
		path = jd["data"]
		base_url = "https://www.proptiger.com/"
		max_page = int(jd["totalCount"])
		cur_page = int(response.url.split(':')[-2].split(',')[0])
		cur_page1 = cur_page + 15
		page_num =str(cur_page1)
		
		url = 'https://www.proptiger.com/data/v2/entity/resale-listing?selector={{%22filters%22:{{%22and%22:[{{%22equal%22:{{%22bookingStatusId%22:1}}}},{{%22equal%22:{{%22cityId%22:18}}}}]}},%22paging%22:{{%22start%22:{x},%22rows%22:15}}}}'.format(x=str(cur_page1))
		
		for i in range(0,len(path)):
			if (i+cur_page) == (max_page):
				break
			item = TigerpropItem()

			item['data_id'] = path[i]['propertyId']
			
			try:
				item['listing_by'] = path[i]['companySeller']['company']['type']
			except:
				item['listing_by'] = 'None'
			
			try:
				item['name_lister'] = path[i]['companySeller']['user']['fullName']
			except:
				item['name_lister'] = 'None'
			
			try:
				item['mobile_lister'] = path[i]['companySeller']['user']['contactNumbers'][0]['contactNumber']
			except:
				item['mobile_lister'] = 'None'

			try:
				item['price_per_sqft'] = path[i]['currentListingPrice']['pricePerUnitArea']
			except:
				item['price_per_sqft'] = '0'

			try:
				item['Selling_price'] = str(path[i]['currentListingPrice']['price'])
			except:
				item['Selling_price'] = '0'

			item['Monthly_Rent'] = '0'

			try:
				dt1 = int(path[i]['currentListingPrice']['createdAt'] * 0.001)
				item['listing_date'] = time.strftime('%m/%d/%Y %H:%M:%S', time.gmtime(dt1))
			except:
				item['listing_date'] = '0'
			
			try:
				dt2 = int(path[i]['currentListingPrice']['updatedAt'] * 0.001)
				item['updated_date'] = time.strftime('%m/%d/%Y %H:%M:%S',time.gmtime(dt2))
			except:
				item['updated_date'] = '0'

			try:
				item['lat'] = path[i]['latitude']
			except:
				item['lat'] = '0'
				
			try:
				item['longt'] = path[i]['longitude']
			except:
				item['longt'] = '0'

			try:
				item['txn_type'] = path[i]['listingCategory']
			except:
				item['txn_type'] = 'None'

			try:
				item['config_type'] = str(path[i]['property']['bedrooms']) + 'BHK'
			except:
				item['config_type'] = 'None'

			try:
				item['property_type'] = path[i]['property']['unitType']
			except:
				item['property_type'] = 'None'

			try:
				item['Bua_sqft'] = str(path[i]['property']['size'])
			except:
				item['Bua_sqft'] = '0'
			try:
				item['carpet_area'] = str(path[i]['property']['carpetArea'])
			except:
				item['carpet_area'] = '0'

			try:
				item['areacode'] = path[i]['property']['project']['localityId']
			except:
				item['areacode'] = 'None'

			try:
				item['city'] = path[i]['property']['project']['locality']['suburb']['city']['label']
			except:
				item['city'] = 'None'

			try:
				item['locality'] = path[i]['property']['project']['locality']['suburb']['label']
			except:
				item['locality'] = 'None'

			try:
				item['sublocality'] = path[i]['property']['project']['locality']['label']
			except:
				item['sublocality'] = 'None'

			try:
				item['Building_name'] = path[i]['property']['project']['locality']['newsTag']
			except:
				item['Building_name'] = 'None'

			try:
				dt3 = int(path[i]['property']['project']['launchDate'] * 0.001)
				item['Launch_date'] = str(time.strftime('%m/%d/%Y %H:%M:%S',time.gmtime(dt3)))
			except:
				item['Launch_date'] = '0'

			try:
				item['address'] = path[i]['property']['project']['address']
			except:
				item['address'] = 'None'

			try:
				dt4 = int(path[i]['property']['project']['possessionDate'] * 0.001)
				item['Possession'] = str(time.strftime('%m/%d/%Y %H:%M:%S',time.gmtime(dt4)))
			except:
				item['Possession'] = '0'
			
			try:
				item['Status'] = path[i]['property']['project']['projectStatus']
			except:
				item['Status'] = 'None'

			try:
				item['platform'] = path[i]['listingSourceDomain']
			except:
				item['platform'] = 'None'

			item['management_by_landlord'] = 'None'

			item['google_place_id'] = 'None'

			item['age'] = 'None'

			if item['Selling_price'] == '0' and item['Monthly_Rent'] == '0':
				item['price_on_req'] = 'true'
			else:
				item['price_on_req'] = 'false'

			item['Details'] = path[i]['property']['project']['description']

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
		
		if (cur_page+15) < ( max_page):
			yield Request(url, callback=self.parse)
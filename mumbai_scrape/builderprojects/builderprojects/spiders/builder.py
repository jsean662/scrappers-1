import scrapy
from builderprojects.items import BuilderprojectsItem
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

class PropSellSpider(Spider):
	name = "BuilderMumbai"
	
	start_urls = [
			'https://www.proptiger.com/app/v2/project-listing?selector={%22filters%22:{%22and%22:[{%22equal%22:{%22builderId%22:100018}},{%22equal%22:{%22builderId%22:100018}}]},%22paging%22:{%22start%22:0,%22rows%22:15}}'
			]
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
		path = jd["data"]["items"]
		base_url = "https://www.proptiger.com/"
		max_page = int(jd["totalCount"])
		cur_page = int(response.url.split(',')[2].split('start')[1].split(':')[1])
		cur_page1 = cur_page + 15
		page_num =str(cur_page1)
		
		url = 'https://www.proptiger.com/app/v2/project-listing?selector={{%22filters%22:{{%22and%22:[{{%22equal%22:{{%22builderId%22:100018}}}},{{%22equal%22:{{%22builderId%22:100018}}}}]}},%22paging%22:{{%22start%22:{x},%22rows%22:15}}}}'.format(x=str(cur_page1))
				
		for i in range(0,len(path)):
			if (i+cur_page) == (max_page):
				break
			item = BuilderprojectsItem()
			count = path[i]['properties']
			c = len(count)
			for j in range(0,c):
			
				item['name_lister'] = 'None'
				item['data_id'] = path[i]['properties'][j]['propertyId']
				item['config_type'] = str(path[i]['properties'][j]['bedrooms']) + "BHK"
				item['property_type'] = path[i]['properties'][j]['unitType']

				item['txn_type'] = "sale"
				dt1 = path[i]['properties'][j]['createdAt']
				number = int(dt1) * 0.001
				dt2 = time.strftime('%m/%d/%Y %H:%M:%S', time.gmtime(number))
				item['listing_date'] = dt2
				dt5 = path[i]['properties'][j]['updatedAt']
				number = int(dt5) * 0.001
				dt2 = time.strftime('%m/%d/%Y %H:%M:%S', time.gmtime(number))
				item['updated_date'] = dt2
				
				try:
					dt1 = path[i]['possessionDate']
					number3 = int(dt1) * 0.001
					dt2 = time.strftime('%m/%d/%Y %H:%M:%S', time.gmtime(number3))				

					item['Possession'] = str(dt2)
				except:
					item['Possession'] = '0'
    	    
				try:
					item['lat'] = path[i]['latitude']
				except KeyError :
					item['lat'] = path[i]['locality']['suburb']['city']['centerLatitude']
				try:
					item['longt'] = path[i]['longitude']
				except KeyError:
					item['longt'] = path[i]['locality']['suburb']['city']['centerLongitude']

				item['Status'] = path[i]['projectStatus']
				item['listing_by'] = 'builder'
				try:
				    item['name_lister'] = path[i]['builder']['name']
				except:
				    item['name_lister'] = 'None'
				
				try:
					item['price_per_sqft'] = path[i]['locality']['avgPricePerUnitArea']
				except:
					item['price_per_sqft'] = '0'
					
				item['Building_name'] = path[i]['builder']['name']+' '+path[i]['name']
				if not path[i]['builder']['name']  in item['Building_name']:
					item['Building_name'] = path[i]['builder']['name']+' '+path[i]['name']
				item['address'] = path[i]['address']
				item['locality'] = path[i]['locality']['suburb']['label']
				item['sublocality'] = path[i]['locality']['label']
				item['city'] = path[i]['locality']['suburb']['city']['label']
				item['areacode'] = path[i]['localityId']
				
				try:
					item['Selling_price'] = str(path[i]['properties'][j]['budget'])
					item['Monthly_Rent'] = '0'
				except KeyError:
					try:
						item['Selling_price'] = str(path[i]['properties'][j]['resalePrice'])
						item['Monthly_Rent'] = '0'
					except KeyError:
						item['Selling_price'] = '0'
						item['Monthly_Rent'] = '0'
				try:
					item['Bua_sqft'] = path[i]['properties'][j]['size']
				except KeyError:
					item['Bua_sqft'] = "0"
				try:
					item['carpet_area'] = path[i]['properties'][j]['carpetArea']
				except KeyError:
					item['carpet_area'] = "0"
				item['platform'] = 'tigerprop'
				item['Details'] = 'None'
				item['Launch_date'] = '0'
				item['age'] = 'None'
				item['google_place_id'] = 'None'
				item['mobile_lister'] = 'None'
				item['management_by_landlord'] = 'None'
				if item['Selling_price'] == '0' and item['Monthly_Rent'] == '0':
				    item['price_on_req'] = 'true'
				else:
				    item['price_on_req'] = 'false'
				
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

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
class purpleyoSpider(Spider):
	name = "propTigerSpider"
	start_urls = [
			'https://www.proptiger.com/app/v2/project-listing?selector={%22filters%22:{%22and%22:[{%22equal%22:{%22cityId%22:18}},{%22equal%22:{%22cityId%22:18}}]},%22paging%22:{%22start%22:0,%22rows%22:15}}'
			]
	allowed_domains = ["www.proptiger.com"]
	rules = (Rule(LinkExtractor(deny=(), allow=('http://www.proptiger.com/'), ), callback='parse', follow=True, ),)
	custom_settings = {
	        'BOT_NAME': 'tigerprop',
	        'DEPTH_LIMIT': 10000,
	        'DOWNLOAD_DELAY': 2
	    }

	def parse(self, response):
		jr = response.body
		jd = json.loads(jr)
		handle_http_list = [500]
		path = jd["data"]["items"]#["groups"]
		base_url = "https://www.proptiger.com/"
		max_page = int(jd["totalCount"])#"propertyid"]["ngroups"])
		cur_page = int(response.url.split(',')[2].split('start')[1].split(':')[1])
		#print max_page,cur_page
		cur_page1 = cur_page + 15
		page_num =str(cur_page1)
		#print page_num
		url = 'https://www.proptiger.com/app/v2/project-listing?selector={{%22filters%22:{{%22and%22:[{{%22equal%22:{{%22cityId%22:18}}}},{{%22equal%22:{{%22cityId%22:18}}}}]}},%22paging%22:{{%22start%22:{x},%22rows%22:15}}}}'.format(x=str(cur_page1))
		#if jd["statusCode"] == "2XX":
		#A = json.load(urllib.urlopen(url))
			#print url
		#url = url.format(page_num=str(cur_page1))
		
		for i in range(0,15):
			if (i+cur_page) == (max_page):
				break
			item = TigerpropItem()
			count = path[i]['properties']
			c = len(count)
			for j in range(0,c):
			
				#url = base_url + url1
				#print str(url)
				#yield item

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
					item['Possession'] = 'None'
    	        #dt3 = dt2.split()[0]
				try:
					item['lat'] = path[i]['latitude']
				except KeyError :
					item['lat'] = path[i]['locality']['suburb']['city']['centerLatitude']
				try:
					item['longt'] = path[i]['longitude']
				except KeyError:
					item['longt'] = path[i]['locality']['suburb']['city']['centerLongitude']

				item['Status'] = path[i]['projectStatus']
				try:
				    item['listing_by'] = path[i]['builder']['mainImage']['title']
				except:
				    item['listing_by'] = 'None'
				
				try:
					item['price_per_sqft'] = path[i]['locality']['avgPricePerUnitArea']
				except:
					item['price_per_sqft'] = 'None'
					
				item['Building_name'] = path[i]['name']
				item['address'] = path[i]['address']
				item['locality'] = path[i]['locality']['suburb']['label']
				item['sublocality'] = path[i]['locality']['label']
				item['city'] = path[i]['locality']['suburb']['city']['label']
				item['areacode'] = path[i]['localityId']
				#print item['areacode']
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
				item['name_lister'] = 'None'
				item['Details'] = 'None'
				item['Launch_date'] = 'None'
				item['age'] = 'None'
				item['google_place_id'] = 'None'
				item['mobile_lister'] = 'None'
				item['management_by_landlord'] = 'None'
				if item['Selling_price'] == '0' and item['Monthly_Rent'] == '0':
				    item['price_on_req'] = 'true'
				else:
				    item['price_on_req'] = 'false'
				
				#item['management_by_landlord'] = path[i]['properties'][j]['management_by_landlord']
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
		#url1 = re
		
		if (cur_page+15) < ( max_page):
			yield Request(url, callback=self.parse)

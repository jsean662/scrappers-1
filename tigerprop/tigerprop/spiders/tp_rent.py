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
	name = "propTigerRentSpider"
	start_urls = ['https://www.proptiger.com/data/v2/entity/resale-listing?selector={%22filters%22:{%22and%22:[{%22equal%22:{%22bookingStatusId%22:1}},{%22equal%22:{%22cityId%22:18}}]},%22paging%22:{%22start%22:0,%22rows%22:15}}']
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
		path = jd["data"]#["items"]#["groups"]
		base_url = "https://www.proptiger.com/"
		max_page = int(jd["totalCount"])#"propertyid"]["ngroups"])
		cur_page = int(response.url.split(':')[-2].split(',')[0])#.split('start')[1].split(':')[1])
		#print cur_page
		#print max_page,cur_page
		cur_page1 = cur_page + 15
		page_num =str(cur_page1)
		#print page_num
		url = 'https://www.proptiger.com/data/v2/entity/resale-listing?selector={{%22filters%22:{{%22and%22:[{{%22equal%22:{{%22bookingStatusId%22:1}}}},{{%22equal%22:{{%22cityId%22:18}}}}]}},%22paging%22:{{%22start%22:{x},%22rows%22:15}}}}'.format(x=str(cur_page1))
		#if jd["statusCode"] == "2XX":
		#A = json.load(urllib.urlopen(url))
			#print url
		#url = url.format(page_num=str(cur_page1))
		
		for i in range(0,15):
			if (i+cur_page) == (max_page):
				break
			item = TigerpropItem()
				#url = base_url + url1
				#print str(url)
				#yield item
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
				item['price_per_sqft'] = 'None'

			try:
				item['Selling_price'] = str(path[i]['currentListingPrice']['price'])
			except:
				item['Selling_price'] = '0'

			item['Monthly_Rent'] = '0'

			try:
				dt1 = int(path[i]['currentListingPrice']['createdAt'] * 0.001)
				item['listing_date'] = time.strftime('%m/%d/%Y %H:%M:%S', time.gmtime(dt1))
			except:
				item['listing_date'] = 'None'
			
			try:
				dt2 = int(path[i]['currentListingPrice']['updatedAt'] * 0.001)
				item['updated_date'] = time.strftime('%m/%d/%Y %H:%M:%S',time.gmtime(dt2))
			except:
				item['updated_date'] = 'None'

			try:
				item['lat'] = path[i]['latitude']
			except:
				item['lat'] = 0
				
			try:
				item['longt'] = path[i]['longitude']
			except:
				item['longt'] = 0

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
				item['Launch_date'] = 'None'

			try:
				item['address'] = path[i]['property']['project']['address']
			except:
				item['address'] = 'None'

			try:
				dt4 = int(path[i]['property']['project']['possessionDate'] * 0.001)
				item['Possession'] = str(time.strftime('%m/%d/%Y %H:%M:%S',time.gmtime(dt4)))
			except:
				item['Possession'] = 'None'
			
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
		
		if (cur_page+15) < ( max_page):
			yield Request(url, callback=self.parse)	

			'''item['config_type'] = str(path[i]['properties'][j]['bedrooms']) + "BHK"
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

					item['immediate_possession'] = str(dt2)
				except:
					item['immediate_possession'] = 'None'
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
				item['Building_name'] = path[i]['name']
				item['address'] = path[i]['address']
				item['locality'] = path[i]['locality']['label']
				item['city'] = path[i]['locality']['suburb']['city']['label']
			
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
					item['sqft'] = path[i]['properties'][j]['size']
				except KeyError:
					item['sqft'] = "0"
				try:
					item['carpet_area'] = path[i]['properties'][j]['carpetArea']
				except KeyError:
					item['carpet_area'] = "0"
				item['platform'] = 'tigerprop'
				item['name_lister'] = 'None'
				item['Details'] = 'None'
				item['sublocality'] = 'None'
				item['age'] = 'None'
				item['google_place_id'] = 'None'
				item['mobile_lister'] = 'None'
				item['areacode'] = 'None'
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
				if ((not item['mobile_lister'] == 'None') or (not item['listing_by'] == 'None') or (not item['name_lister'] == 'None')):
				    item['quality3'] = 1
				else:
				    item['quality3'] = 0
				yield item
		#url1 = re
		
		if (cur_page+14) < ( max_page):
			yield Request(url, callback=self.parse)'''

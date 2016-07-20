import scrapy
from purpl.items import PurplItem
from scrapy.spiders import Spider
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.selector import Selector
from scrapy.selector import HtmlXPathSelector
from scrapy.http import Request
from datetime import datetime as dt
from datetime import time,timedelta
from datetime import date
import time
import json
from scrapy.selector import XmlXPathSelector
import lxml.etree as etree
from urlparse import urljoin
class purpleyoSpider(Spider):
	name = "purpl"
	start_urls = [
			'http://www.purpleyo.com/solr/search?q=Mumbai+India&rows=8&searchtype=resultpage&sort=listingtype+asc,plantype+asc,listingstatus+asc,+issizeavailable+desc,+random_1466580605918+desc,+total_available_size+desc,+viewcount+desc,+updated_at+desc,+pyoindex+desc&start=0&url=http:%2F%2F172.31.17.31%2Fsolr%2Fcollection1%2Fselect%3Ffq%3Dlocaleid:1%26fq%3Dpyoindex:%5B0+TO+1000%5D%26fq%3D(total_available_size:%5B*+TO+*%5D+OR+sizeavailable:%5B*+TO+*%5D)%26fq%3Dcity:%22Mumbai%22%26fq%3Dstatus:%22ACTIVE%22%26fq%3Dpropertytype:(%22OFFICE%22+OR+%22RETAIL%22+OR+%22OFFICE+AND+RETAIL%22)%26fq%3Davailability:("SALE"+OR+"LEASE"+OR+"LEASE%2FSALE")%26start%3D0&wt=json'
			]
	allowed_domains = ["www.purpleyo.com"]
	rules = (Rule(LinkExtractor(deny=(), allow=('http://www.purpleyo.com/'), ), callback='parse_item', follow=True, ),)
	custom_settings = {
	        'BOT_NAME': 'purpleyo',
	        'DEPTH_LIMIT': 1000,
	        'DOWNLOAD_DELAY': 0
	    }

	def parse(self, response):
		jr = response.body
		jd = json.loads(jr)
		path = jd["grouped"]["propertyid"]["groups"]
		
		max_page = int(jd["grouped"]["propertyid"]["ngroups"])
		cur_page = int(response.url.split('&')[4].split('=')[-1])
		url = 'http://www.purpleyo.com/solr/search?q=Mumbai+India&rows=8&searchtype=resultpage&sort=listingtype+asc,plantype+asc,listingstatus+asc,+issizeavailable+desc,+random_1466580605918+desc,+total_available_size+desc,+viewcount+desc,+updated_at+desc,+pyoindex+desc&start={page_num}&url=http:%2F%2F172.31.17.31%2Fsolr%2Fcollection1%2Fselect%3Ffq%3Dlocaleid:1%26fq%3Dpyoindex:%5B0+TO+1000%5D%26fq%3D(total_available_size:%5B*+TO+*%5D+OR+sizeavailable:%5B*+TO+*%5D)%26fq%3Dcity:%22Mumbai%22%26fq%3Dstatus:%22ACTIVE%22%26fq%3Dpropertytype:(%22OFFICE%22+OR+%22RETAIL%22+OR+%22OFFICE+AND+RETAIL%22)%26fq%3Davailability:("SALE"+OR+"LEASE"+OR+"LEASE%2FSALE")%26start%3D{page_num}&wt=json'.format(page_num=str(cur_page+8))	
		
		for i in range(0,8):
			if (i+cur_page) == max_page:
				break
			item = PurplItem()
			#item['desc'] = path[i]['doclist']['docs'][0]
			item['data_id'] = path[i]['doclist']['docs'][0]['propertyid']
			item['property_type'] = path[i]['doclist']['docs'][0]['propertytype']
			item['txn_type'] = path[i]['doclist']['docs'][0]['availability']
			dates = path[i]['doclist']['docs'][0]['updated_at'].replace("T"," ").replace("Z","")
			item['listing_date'] = dt.strftime(dt.strptime(dates,"%Y-%m-%d %H:%M:%S"),"%m/%d/%Y %H:%M:%S") 
			item['lat'] = path[i]['doclist']['docs'][0]['lat']
			item['longt'] = path[i]['doclist']['docs'][0]['lng']
			item['Status'] = path[i]['doclist']['docs'][0]['construction_status']
			item['Building_name'] = path[i]['doclist']['docs'][0]['name']
			item['address'] = path[i]['doclist']['docs'][0]['address1']
			item['areacode'] = path[i]['doclist']['docs'][0]['areacode']
			item['city'] = path[i]['doclist']['docs'][0]['city']
			item['locality'] = path[i]['doclist']['docs'][0]['locality']
			item['sqft'] = path[i]['doclist']['docs'][0]['total_size']
			item['platform'] = 'purpleyo'
			item['management_by_landlord'] = path[i]['doclist']['docs'][0]['management_by_landlord']
			item['config_type'] = 'None'
			item['Selling_price'] = '0'
			item['Monthly_Rent'] = '0'
			item['price_on_req'] = 'false'
			item['listing_by'] = 'None'
			item['name_lister'] = 'None'
			item['Details'] = 'None'
			item['sublocality'] = 'None'
			item['age'] = 'None'
			item['google_place_id'] = 'None'
			item['immediate_possession'] = 'None'
			item['mobile_lister'] = 'None'
			item['carpet_area'] = 'None'
			item['listing_date'] = item['listing_date']
			
			yield item

		if (cur_page+8) < max_page:
			yield Request(url, callback=self.parse)

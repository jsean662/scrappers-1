import scrapy
import logging
from acres.items import AcresItem
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

class JagahaSpider(CrawlSpider):
	name = "acresSpider"
	allowed_domains = ['99acres.com']

	start_urls = [
			'http://www.99acres.com/property-in-mumbai-ffid-page-1?orig_property_type=R&class=O,A,B&search_type=QS&search_location=CP12&lstacn=SEARCH&pageid=QS&search_id=7019357638975910&src=PAGING&lastAcn=SEARCH&lastAcnId=7019357638975910' , 
			'http://www.99acres.com/rent-property-in-mumbai-ffid-page-1?orig_property_type=R&class=O,A,B&search_type=QS&search_location=CP12&pageid=QS&search_id=7024716630429298&src=PAGING&lastAcn=SEARCH&lastAcnId=7024716630429298&fsl_results=Y&total_fsl_count=2'
			#'http://www.99acres.com/commercial-property-in-mumbai-ffid-page-1?orig_property_type=C&class=O,A,B&search_type=QS&search_location=SH&lstacn=SEARCH&pageid=QS&search_id=7025026338708533&src=PAGING&lastAcn=SEARCH&lastAcnId=7025026338708533&fsl_results=Y&total_fsl_count=2',
			#'http://www.99acres.com/rent-commercial-property-in-mumbai-ffid-page-1?orig_property_type=C&class=O,A,B&search_type=QS&search_location=SH&lstacn=SEARCH&pageid=QS&keyword_orig=mumbai&search_id=7025187469574654&src=PAGING&lastAcn=SEARCH&lastAcnId=7025187469574654&fsl_results=Y&total_fsl_count='
			]
	custom_settings = {
			'BOT_NAME': 'acres',
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
		
		for i in x:
			item = AcresItem()
			#self.data_list.append(data_id)
			data_id = i.xpath("@data-propid").extract_first()
			sqft_check = i.xpath("div[@class='srpDetail']/div[@class='srpDataWrap']/span[1]/b[1]/text()").extract_first().replace("Sq.Ft.","").replace("Sq. Meter","").strip()
			check = 0
			#print sqft_check
			if 'to' in sqft_check:
				sqft1 = str(sqft_check.split('to')[0]).strip()
				sqft2 = str(sqft_check.split('to')[1]).strip()
				#print sqft1,sqft2
				sqft_list = [sqft1,sqft2]
				#print sqft_list
			else:
				sqft_list = [sqft_check]
				#print sqft_list
			for s in sqft_list:
				check = check + 1    
				
				'''
				Assign Default values
				'''
				item['Possession'] = 'None'
				item['txn_type'] = 'None'
				item['Status'] = 'None'
				item['age'] = 'None'
				item['lat'] = 0
				item['longt'] = 0
				item['address'] = 'None'
				item['sublocality'] = 'None'
				item['google_place_id'] = 'None'
				item['Launch_date'] = 'None'
				item['mobile_lister'] = 'None'
				item['areacode'] = 'None'
				item['management_by_landlord'] = 'None'
				item['carpet_area'] = 0

				item['data_id'] = data_id
				
				item['platform'] = '99acres'
				
				item['property_type'] = x1.xpath("span[@id='ysfPropertyType']/b/text()").extract_first().split(" ")[1]
				
				item['city'] = x1.xpath("span[3]/b/text()").extract_first().split(" ")[0]
			
				item['Bua_sqft'] =  s
				
				try:
					item['price_per_sqft'] = i.xpath("div[@class='srpDetail']/div[@class='srpDataWrap']/span/text()").extract()[2].replace(' / Sq.Ft.','').replace('/','').strip()
					#print item['price_per_sqft']
					if item['price_per_sqft'] == '':
						item['price_per_sqft'] = 0
				except:
					item['price_per_sqft'] = 0                       
				try:
					item['Building_name'] = str(i.xpath("div[@class='srpDetail']/div[@class='srpDataWrap']/span[2]/a[@class='sName']/b/text()").extract_first()).strip()
				except:
					try:
						item['Building_name'] = str(i.xpath("div[@class='srpDetail']/div[@class='srpDataWrap']/span[2]/b/text()").extract_first()).strip()
					except:
						item['Building_name'] = 'None'
				if item['Building_name'] == '':
					item['Building_name'] = 'None'


				stat1 = i.xpath("div[@class='srpDetail']/div[@class='srpDataWrap']/span[3]/span/text()").extract()
				stat2 = i.xpath("div[@class='srpDetail']/div[@class='srpDataWrap']/span[2]/span/text()").extract()
				
				try:
					if stat1:
						item['txn_type'] = stat1[1].encode('ascii', 'ignore').decode('ascii').replace('On ','')
						if 'New' in item['txn_type']:
							item['txn_type'] = 'Sale'

						if 'ale' in item['txn_type']:

							item['Status'] = stat1[3].strip()
							
							if 'Construction' in item['Status']:
								poss = stat1[5].strip().split('By ')[-1]
								item['Possession'] = dt.strftime(dt.strptime(poss,'%b %Y'),'%m/%d/%Y %H:%M:%S')
								item['age'] = 'None'
							elif 'move' in item['Status']:
								item['age'] = stat1[5].strip()
								item['Possession'] = 'None'
						elif 'ent' in item['txn_type']:

							item['Possession'] = 'None'

							item['Status'] = stat1[5].strip()

							item['age'] = stat1[3].strip()
				except:
					print stat1

				try:
					if stat2:
						item['txn_type'] = stat2[1].encode('ascii', 'ignore').decode('ascii').replace('On ','')
						if 'New' in item['txn_type']:
							item['txn_type'] = 'Sale'

						if 'ale' in item['txn_type']:

							item['Status'] = stat2[3].strip()
							
							if 'Construction' in item['Status']:
								poss = stat2[5].strip().split('By ')[-1]
								item['Possession'] = dt.strftime(dt.strptime(poss,'%b %Y'),'%m/%d/%Y %H:%M:%S')
								item['age'] = 'None'
							elif 'move' in item['Status']:
								item['age'] = stat2[5].strip()
								item['Possession'] = 'None'
						elif 'ent' in item['txn_type']:

							item['Possession'] = 'None'

							item['Status'] = stat2[5].strip()

							item['age'] = stat2[3].strip()
				except:
					print stat2
				
				detail1 = i.xpath("div[@class='srpDetail']/div[@class='srpDataWrap']/div[4]/b/text()").extract_first()
				if (not detail1==None) and ('Description :' in detail1):
					item['Details'] = i.xpath("div[@class='srpDetail']/div[@class='srpDataWrap']/div[4]/text()").extract()[-1].strip()
				else:
					detail2 = i.xpath("div[@class='srpDetail']/div[@class='srpDataWrap']/div[3]/b/text()").extract_first()
					if (not detail2==None) and ('Description :' in detail2):
						item['Details'] = i.xpath("div[@class='srpDetail']/div[@class='srpDataWrap']/div[3]/text()").extract()[-1].strip()
					else:
						item['Details'] = 'None'
				
				if item['property_type'] == 'Residential':
					conf1 = i.xpath("div[@class='wrapttl']/div[1]/a/text()").extract_first().split(',')[0].strip()
					conf2 = i.xpath("div[@class='wrapttl']/div[1]/a/text()").extract_first().split(')')[0].split('(')[-1].strip()
					if ('BHK' in conf1):
						item['config_type'] = conf1
					elif ('RK' in conf2):
						item['config_type'] = conf2
					elif 'Bedroom' in conf1:
						item['config_type']  = conf1.split(" ")[0] + ' BHK'
					else:
						item['config_type'] = 'None'
				else:
					item['config_type'] = 'None'
				
				item['locality'] = i.xpath("div[@class='wrapttl']/div[1]/a/text()").extract_first().split(' in ')[-1].strip()
				
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
					logging.log(logging.ERROR,build)
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
					item['listing_date'] = 'None'
					item['updated_date'] = 'None'
				
				price = i.xpath("div[@class='wrapttl']/div[1]/span/b[2]/text()").extract_first()
				#print price
				if price:
					if 'to' in price:
						price1 = price.split('to')[0]
						price2 = price.split('to')[1]
					
						if 'Lac' in price1:
							price1 = float(str(price1.split()[0])) * 100000
						else:
							if 'Crore' in price1:
								price1 =  float(str(price1.split()[0])) * 10000000
						if 'Lac' in price2:
							price2 = float(str(price2.split()[0])) * 100000
						else:
							if 'Crore' in price2:
								price2 =  float(str(price2.split()[0])) * 10000000 
						#print price1 , price2
						if check == 1:
							price = str(price1)
						else:
							price = str(price2)
					else:
						if 'Lac' in price:
							price = str(float(str(price.split()[0])) * 100000)
						else:
							if 'Crore' in price:
								price =  str(float(str(price.split()[0])) * 10000000)
					if (('Rent' in item['txn_type']) or ('Lease' in item['txn_type'])):
						item['Monthly_Rent'] = price.replace(',','')
						item['Selling_price'] = '0'
					else:
						item['Selling_price'] = price
						item['Monthly_Rent'] = '0'
				else:
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
					item['longt'] = 0
				
								
				if ((not item['Building_name'] == 'None') and (not item['listing_date'] == 'None') and (not item['txn_type'] == 'None') and (not item['property_type'] == 'None') and ((not item['Selling_price'] == '0') or (not item['Monthly_Rent'] == '0'))):
					item['quality1'] = 1
				else:
					item['quality1'] = 0
	
				if ((not item['Launch_date'] == 'None') or (not item['Possession'] == 'None')):
					item['quality2'] = 1
				else:
					item['quality2'] = 0

				if ((not item['mobile_lister'] == 'None') or (not item['listing_by'] == 'None') or (not item['name_lister'] == 'None')):
					item['quality3'] = 1
				else:
					item['quality3'] = 0
				yield item
				
		curPage = int(response.url.split('?')[0].split('-')[-1])
		maxPage = str(response.xpath("//div[@class='lcol_new']/div[@class='pgdiv']/a[last()-1]/text()").extract_first())
		if maxPage == 'None':
			maxPage = curPage+1
		#print maxPage
		#print response.body
		if curPage < maxPage :
			if 'rent-property' in response.url:
				next_url = 'http://www.99acres.com/rent-property-in-mumbai-ffid-page-{x}?orig_property_type=R&class=O,A,B&search_type=QS&search_location=CP12&pageid=QS&search_id=7024716630429298&src=PAGING&lastAcn=SEARCH&lastAcnId=7024716630429298&fsl_results=Y&total_fsl_count=2'.format(x=str(curPage+1))
				yield Request(next_url,callback=self.parse)
			else:
				if 'property' in response.url:
					next_url = 'http://www.99acres.com/property-in-mumbai-ffid-page-{x}?orig_property_type=R&class=O,A,B&search_type=QS&search_location=CP12&lstacn=SEARCH&pageid=QS&search_id=7019357638975910&src=PAGING&lastAcn=SEARCH&lastAcnId=7019357638975910'.format(x=str(curPage+1))
					yield Request(next_url,callback=self.parse)
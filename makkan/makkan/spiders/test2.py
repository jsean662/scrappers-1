import scrapy
from scrapy import log
from urlparse import urljoin
from scrapy.spiders import Spider
from scrapy.http import Request
from scrapy.exceptions import CloseSpider
from scrapy.spiders import CrawlSpider, Rule
from scrapy.selector import HtmlXPathSelector
from scrapy.http import Request
from scrapy.linkextractors import LinkExtractor
from scrapy.selector import Selector
from makkan.items import Website
from scrapy.loader import ItemLoader
import time
import unicodedata
import time
import datetime
from datetime import datetime as dt
class SeekingAlpha(CrawlSpider):
    name = "s2"
    
    allowed_domains = ['makaan.com']

    
    

    start_urls = [  
                   "https://www.makaan.com/listings?listingType=buy&pageType=LISTINGS_PROPERTY_URLS&cityName=Mumbai&cityId=18&templateId=MAKAAN_CITY_LISTING_BUY&page=1",
                   "https://www.makaan.com/listings?listingType=rent&pageType=CITY_URLS&cityName=Mumbai&cityId=18&templateId=MAKAAN_CITY_LISTING_BUY&page=1"
                    
        ]     
    data_id_list = []
            
    #for i in range(2, 40) :
        #start_urls.append(start_urls + "/?page=" + i)

   
    
    rules = (Rule(LinkExtractor(deny=(), allow=('http://www.makaan.com/'),), callback='parse_item', follow=True, ),)
   
    
  #  def parse(self, response):
        
     
    def parse(self, response):
        #self.log("Scraping: %s" % response.url, level=log.INFO)
        #time.sleep(2.5)
        handle_httpstatus_list = [404 , 502, 500 , 408, 400] 
        hxs = Selector(response)
        P = "//div[@class='cardholder']"
        a = hxs.xpath(P)
        sale = hxs.xpath("//div/div[@class='srow']/div/div[@class='f-count-wrap']/h1/text()").extract_first()
        c1 = dt.strftime(dt.strptime("2015-01-01","%Y-%m-%d"),"%m/%d/%Y")
        c2 = dt.strftime(dt.strptime(str(dt.now().date()),"%Y-%m-%d"),"%m/%d/%Y")
        
        for i in a:
            base_url = "https://www.makaan.com"
            
            item = Website()
            s = i.xpath("div/script/text()").extract_first()
            
            dt5 = s.split('"postedDate"')[1].split(',')[0].split('"')[1]#[-21].split('"')[1]
          #  print dt5
            number = int(dt5) * 0.001
            dt2 = time.strftime('%m/%d/%Y %H:%M:%S', time.gmtime(number))
            
            dt3 = dt2.split()[0]

          #  print dt1

            if c1 < dt3 < c2:
                data_id = i.xpath('div/@data-listing-id').extract()
                if data_id not in self.data_id_list:
                    self.data_id_list.append(data_id)

                    item['listing_date'] = dt2
                    
                    
                    
                    
                    item['platform'] = 'makaan'
                    
                    item['txn_type'] = sale.split('in Mumbai')[0].split('for')[1]
                    item['data_id'] = i.xpath("div/@data-listing-id").extract()
                    
                    sell = i.xpath("div/div/div[2]/div[1]/div[1]/div[1]/div[1]/div/span[1]/meta[1]/@content").extract_first()
                    
                   
                    if sell.find("Cr") :
        	        	sell1 = i.xpath("div/div/div[2]/div[1]/div[1]/div[1]/div[1]/div/span[1]/meta[1]/@content").extract_first().split()[-1]
        	        	if sell1 == 'Cr':
        	        		sell2 = sell.split()[0]
        	        		sell3 = float(sell2)*10000000
        	        		item['Selling_price']= str(sell3)
                		elif sell1 =='L':
                			sell2 = sell.split()[0]
                			sell3 = float(sell2)*100000
        	        		item['Selling_price'] = str(sell3)
        	        	else:
        	        		sell2 = sell
        	        		item['Selling_price'] = str(sell2)

                  
             	
                    item['price_per_sqft'] = i.xpath("div/div/div[2]/div[1]/div[1]/div[1]/div[2]/span/text()").extract()
                    item['config_type'] = i.xpath("div/div/div[2]/div[1]/div[2]/div/h2/a/span/span/text()").extract()
                    try:
                            item['Bua_sqft'] = i.xpath("div/div/div[2]/div[1]/div[2]/span/text()").extract_first().replace("sq ft","")
                    except AttributeError:
                            item['Bua_sqft'] = '0'
                    item['Building_name'] = str(i.xpath("div/div/div[2]/div[2]/div/span[1]/a/span/text()").extract_first())
                    if item['Building_name'] == '':
                        item['Building_name'] = 'None'
                    item['locality'] = i.xpath("div/div/div[2]/div[2]/div/span/span[1]/a/span/text()").extract()
                    r = i.xpath("div/div/div[2]/div[2]/div/span/span[2]/text()").extract_first()
                    item['city'] = r.encode('ascii','ignore')#.replace('\\xa0', ' ')
                    s = i.xpath("div/div/div[2]/div[3]/div[1]/div[1]/text()").extract_first()
                    item['Status'] = s
                    item['age'] = 'None'
                    if s == 'Ready to move':
                        item['age'] = str(i.xpath("div/div/div[2]/div[3]/div[@class='dcol age']/div[1]/text()").extract_first().strip())
                        
                    item['name_lister'] = i.xpath("div/div/div[4]/div/div[2]/span[1]/text()").extract()
                    r1 = i.xpath("div/div/div[4]/div/div[2]/span[2]/text()").extract()
                    item['listing_by'] = str(r1).split("(")[1].split(")")[0]
                    item['mobile_lister'] = i.xpath("div/div/div[4]/div[2]/a/@data-sellerphone").extract_first()
                    item['property_type'] = 'Residential'
                    item['Details'] = 'None'
                    item['Monthly_Rent'] = '0'
                    item['carpet_area'] = 'None'
                    item['management_by_landlord'] = 'None'
                    item['updated_date'] = item['listing_date']
                    item['areacode'] = 'None'
                    item['google_place_id'] = 'None'
                    item['Launch_date'] = 'None'
                    item['Possession'] = 'None'
                    item['address'] = 'None'
                    item['sublocality'] = 'None'
                    
                    if item['Selling_price'] == '0' and item['Monthly_Rent'] == '0':
                        item['price_on_req'] = 'true'
                    else:
                        item['price_on_req'] = 'false'
                    s1 = i.xpath("div/script/text()").extract_first()
                    dt1 = s1.split('"listingUrl"')[1].split(',')[0].split('"')[1]
                    #print dt1

                    
                    url1 = base_url + str(dt1)


                    yield Request(url1, callback=self.parse_item,  meta={'item': item}, dont_filter = True)
                
                sel = Selector(response)
               
                item = Website()
                listing_count = sel.xpath('//div[@class="list-mainarea"]/div[@data-module="listingsWrapper"]/script/text()').extract_first().split()[1].split('"listingCount":')[-1]
                max_page = sel.xpath('//div[@class="search-result-footer"]/div[@data-module="pagination"]/script/text()').extract_first().split()[1].split('"totalPages":')[-1]

                if int(listing_count) != 0:
            
                    url = response.url.split('&')
                    page = url[-1].split("=")
                    #print page
                    
                    page[-1] = str(int(page[-1]) + 1)
                    if int(page[-1]) < int(max_page):
                        url[-1] = '='.join(page)
                        url = '&'.join(url)
                        yield Request(url,callback=self.parse)
            
        
    def parse_item(self,response):
        
    
        hxs = Selector(response)
        item = response.meta['item']
        P = "//div[@class='map-area']"

        a = hxs.xpath(P)
        for i in a:
            s = i.xpath("div[@data-module='mapsModule']/script/text()").extract()
            item['lat'] = str(s).split('"')[3]
            item['longt'] = str(s).split('"')[7]

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
        

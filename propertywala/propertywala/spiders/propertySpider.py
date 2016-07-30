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
from propertywala.items import PropertywalaItem
from scrapy.loader import ItemLoader
import time
from datetime import date
class SeekingAlpha(CrawlSpider):
    name = "s1"
    download_delay = 0.1

    more_pages = True
    next_page = 1
    allowed_domains = ['propertywala.com']
    
    

    start_urls = [  
                    
                    "https://www.propertywala.com/properties/type-residential/for-sale/location-mumbai_maharashtra?page=1",
                    "https://www.propertywala.com/properties/type-residential/for-rent/location-mumbai_maharashtra?page=1",
                    "https://www.propertywala.com/properties/type-commercial/for-rent/location-mumbai_maharashtra?page=1",
                    "https://www.propertywala.com/properties/type-commercial/for-sale/location-mumbai_maharashtra?page=1"
        ]     
    data_id_list = [] 
    #for i in range(2, 40) :
        #start_urls.append(start_urls + "/?page=" + i)

   
    
    rules = (Rule(LinkExtractor(deny=(), allow=('http://www.propertywala.com/properties'),), callback='parse', follow=True, ),)
    
    base_url = "https://www.propertywala.com"
    
    def parse(self, response):
        base_url = "https://www.propertywala.com/"
        
        c1 = time.strptime("2015-01-01","%Y-%m-%d")
        c2 = time.strptime(str(date.today()),"%Y-%m-%d")
        hxs = Selector(response)
        P = "//body/div/article/div[@id='propertyList']/article"
        a = hxs.xpath(P)
    
        
        for i in a:
            
            item = PropertywalaItem()

            c3 = i.xpath("div[@class='summary']/ul/li[@class='posted']/time/@datetime").extract_first()
            if  c1 < c3 :
                data_id = i.xpath('@id').extract()
                if data_id not in self.data_id_list:
                    self.data_id_list.append(data_id)
    	            item['listing_date'] = str(c3)
    	            item['data_id'] = i.xpath("@id").extract_first()
    	            item['platform'] = 'propertywala'
    	            x = response.url.split('/')[4]
    	            item['property_type'] = x.split('-')[-1]
    	            p = response.url.split('/')[-1]
    	            tp = p.split('-')[-1]
    	            if "?" not in tp :
    	                item['city'] = tp.split('_')[0]
    	            else :
    	                item['city'] = tp.split('?')[0].split('_')[0]
    	      
    	      
    	            item['sqft'] = i.xpath("div[@class='summary']/ul/li[@class='features']/span[@class='areaUnit']/text()").extract_first()
    	            if item['sqft'] == 'None':
    	                item['sqft'] = '0'
    	            	             	       
    	            r = i.xpath("div[@class='summary']/ul/li[@class='contact']/button/@title").extract_first()
    	            r1 = str(r).split()[-1].split("(")[1].split(")")[0]
    	            if r1 == "1" :
    	                item['listing_by'] = ''
    	            else :
    	                item['listing_by'] = r1
    	           
    	            item['listing_date'] = i.xpath("div[@class='summary']/ul/li[@class='posted']/time/@datetime").extract()
    	           
    	 #           dlt = ("".join(i.xpath("header/div[@class='propertysell']/text()").extract())).replace( '\r\n', '').replace( ' ', '').replace("u'","")
    	            
    	           # ddt = map(unicode.strip , dlt)

    	#            item['selling_sell'] = dlt
    	          
    	            item['Building_name'] = i.xpath("div[@class='summary']/ul/li[@class='title']/a/text()").extract_first() 
    	            z = ("".join(i.xpath("header/h4/a/text()").extract()))
    	            g = str(z).split(', Mumbai')[0]
    	           
    	            
    	            item['Details'] = g.replace("\r\n","").strip()



    	            y = response.url.split('/')[5]
    	            
    	            item['txn_type'] = y.split('-')[1]
    	            

    	            if item['txn_type'] in ['rent']:

    	                item['locality'] = str(g).split("rent in")[1]

    	            if item['txn_type'] in ['sale']:
    	                item['locality'] = str(g).split("sale in")[1]            
    	            
    	            slt = i.xpath("header/h4/a/text()").extract()
    	            t = str(slt).split()[1]
    	            if item['property_type'] in ['residential'] :
    	                if str(t).isdigit():
    	                    item['config_type'] = t + "bhk"
    	            if item['property_type'] in ['commercial'] :
    	                item['config_type'] = 'None'
    	            item['name_lister'] = i.xpath("div[@class='summary']/ul/li[@class='posted']/a/text()").extract()
    	           
    	            urlid = base_url + item['data_id']
    	            
    	           # yield item
    	            yield Request(urlid, callback=self.parse_item1,  meta={'item': item}, dont_filter = True)
                sel = Selector(response)
                item = PropertywalaItem()
                url1 = response.url.split("/")[6]
                url = url1.split("?")
                url2 = response.url.split("?")[0]
                d = sel.xpath("//body/div/article/div[@id='propertyList']/div[@class='searchPanel clearfix'][1]/div[@class='paging']/a[position() = last()]/@href").extract_first()
                max_limit = int(d.split('?')[1].split('=')[1])
                counter = int(url[1].split('=')[1])
                page_num = counter + 1
                url[1] = '?page={page_num}'.format(page_num=page_num)
                url =   url2  + url[1]
                if counter < max_limit :
                	yield Request(url, callback=self.parse)
                else :
                	yield Request(url2,callback= self.parse_item)



        
    #url = urlparse.urljoin(string, x)
            #yield Request(url, callback=parse_item1)
    
    def parse_item(self, response):
        #self.log("Scraping: %s" % response.url, level=log.INFO)
        base_url = "https://www.propertywala.com/"
        c1 = time.strptime("2015-01-01","%Y-%m-%d")
        c2 = time.strptime(str(date.today()),"%Y-%m-%d")
        hxs = Selector(response)
        P = "//body/div/article/div[@id='propertyList']/article"
        a = hxs.xpath(P)
        for i in a:
            
            item = PropertywalaItem()

            c3 = i.xpath("div[@class='summary']/ul/li[@class='posted']/time/@datetime").extract_first()
            if  c1 < c3 < c2  :
                data_id = i.xpath('id').extract()
                if data_id not in self.data_id_list:
                    self.data_id_list.append(data_id)
    	            item['listing_date'] = str(c3)
    	            item['data_id'] = i.xpath("@id").extract_first()
    	            item['platform'] = 'propertywala'
    	            x = response.url.split('/')[4]
    	            item['property_type'] = x.split('-')[-1]
    	            p = response.url.split('/')[-1]
    	            tp = p.split('-')[-1]
    	            if "?" not in tp :
    	                item['city'] = tp.split('_')[0]
    	            else :
    	                item['city'] = tp.split('?')[0].split('_')[0]
    	      
    	      
    	            item['sqft'] = i.xpath("div[@class='summary']/ul/li[@class='features']/span[@class='areaUnit']/text()").extract_first()
                    if item['sqft'] == 'None':
                        item['sqft'] = '0'    	        
    	         
    	       
    	            r = i.xpath("div[@class='summary']/ul/li[@class='contact']/button/@title").extract_first()
    	            r1 = str(r).split()[-1].split("(")[1].split(")")[0]
    	            if r1 == "1" :
    	                item['listing_by'] = ''
    	            else :
    	                item['listing_by'] = r1
    	            item['listing_date'] = i.xpath("div[@class='summary']/ul/li[@class='posted']/time/@datetime").extract()
    	           
    	            
    	           

    	            y = response.url.split('/')[5]
    	            
    	            item['txn_type'] = y.split('-')[1]
    	          
    	            item['Building_name'] = i.xpath("div[@class='summary']/ul/li[@class='title']/a/text()").extract_first() 
    	            z = ("".join(i.xpath("header/h4/a/text()").extract()))
    	            g = str(z).split(', Mumbai')[0]
    	            
    	            item['Details'] = g.replace("\r\n","").strip()
    	            if item['txn_type'] in ['rent']:
    	                item['locality'] = str(g).split("rent in")[1]

    	            if item['txn_type'] in ['sale']:
    	                item['locality'] = str(g).split("sale in")[1]           
    	            

    	            slt = i.xpath("header/h4/a/text()").extract()
    	            t = str(slt).split()[1]
    	            if item['property_type'] in ['residential'] :
    	                if str(t).isdigit():
    	                    item['config_type'] = t +"bhk"
    	            if item['property_type'] in ['commercial'] :
    	                item['config_type'] = 'None'
    	            item['name_lister'] = i.xpath("div[@class='summary']/ul/li[@class='posted']/a/text()").extract()
    	        
    	             
    	            urlid = base_url + item['data_id']
    	            
    	            yield Request(urlid, callback=self.parse_item1,  meta={'item': item}, dont_filter = True)

    def parse_item1(self, response):  

        hxs = Selector(response)
        item = response.meta['item']

        path = "//div/article/div/div[@id='PropertyDetails']/section[@id='PropertySummary']/ul"
        rt = hxs.xpath(path)
        
        if "#"  not in str(response.url):
        	
            rt1 = rt.xpath('li[contains(text(),"Monthly Rent:")]/span/text()').extract_first()
            if rt1:
            	if '-' in rt1:
                    sell1 = rt1.split('-')[0]
                    sell2 = rt1.split('-')[1]
                    #ell3 = str(sell1)
                    #sell4 = str(sell2)

                    
                    if 'lacs' in sell2:
                        sell1 = float(sell1) * 100000 
                        sell2 =  float(sell2.split()[0]) * 100000
                        rt1 = int(float((sell1 + sell2)/2))
                    else:
            			if 'lac' in sell2:
            				sell2 = float(sell2.split()[0]) *100000
            				rt1 = int(float((sell1 + sell2)/2))
    				else:
                        
    					rt1 = sell1
					item['Monthly_Rent'] = str(rt1)
                else:
                    if 'Above' in rt1:
                        r1 = rt1.split()[1]
                        rt1 = float(r1)*100000
                    item['Monthly_Rent'] = str(rt1)
              	
	            item['Monthly_Rent'] = str(rt1)

            else:
                item['Monthly_Rent'] = '0'
            
            sell = rt.xpath('li[contains(text(),"Price:")]/span/text()').extract_first()
            if sell:
            	if '-' in sell:
                    sell1 = sell.split('-')[0]
                    sell2 = sell.split('-')[1]
                    
                    if 'lacs' in sell2:
                        sell1 = float(sell1) * 100000 
                        sell2 =  float(sell2.split()[0]) * 100000
                        sell = int(float((sell1 + sell2)/2))
                    else:
                        if 'crores' in sell2:
                        	sell1 = float(sell1) * 10000000 
                        	sell2 =  float(sell2.split()[0]) * 10000000
                    		sell = int(float((sell1 + sell2)/2))
            		else:
            			if 'crore' in sell2:
            				sell1 = float(sell1) * 10000000 
                        	sell2 =  float(sell2.split()[0]) * 10000000
                    		sell = int(float((sell1 + sell2)/2))

                	item['Selling_price'] = str(sell)
            	else:
            		if 'Below' in sell:
            			sell1 = sell.split()[1]
            			sell = float(sell1)*100000
    				item['Selling_price'] = str(sell)
    			else:
    				item['Selling_price'] = str(sell)   		
            else:
                item['Selling_price'] = '0'
            rt3 = rt.xpath('li[contains(text(),"Furnished:")]/span/text()').extract()
            item['Status'] = rt3
            rt4 = rt.xpath('li[contains(text(),"Lease Period:")]/span/text()').extract()
            item['lease_period'] = rt4
            rt5 = rt.xpath('li[contains(text(),"Available:")]/span/text()').extract()
            #item['availability'] = rt5
            #item['immediate_possession'] = rt5
            #print item['availability']
            rt6 = rt.xpath('li[contains(text(),"Possession:")]/span/text()').extract()
            item['Possession'] = rt6 + rt5
            #print item['immediate_possession']
            rt7 = rt.xpath('li[contains(text(),"Age of Construction:")]/span/text()').extract()
            item['age'] = rt7
            
            yield item
        
     

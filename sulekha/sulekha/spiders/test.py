from scrapy.spiders import BaseSpider
from scrapy.selector import Selector
from sulekha.items import PropertyItem
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors.sgml import SgmlLinkExtractor
from datetime import datetime

class MySpider(CrawlSpider):
    name = "SulekhaSpider"
    allowed_domains = ['property.sulekha.com']
    start_urls = ["http://property.sulekha.com/property-in-mumbai-for-sale",
   ]
   #"//*[@id="pagediv"]/ul/li[6]/a"
    rules = (
        Rule(SgmlLinkExtractor(allow=('property.sulekha.com'), restrict_xpaths=('//*[@id="listings-wrap"]/li/div[2]/div[2]/ul[1]/li[3]/a[@href]','//*[@id="listings-wrap"]/li/div[2]/div[2]/ul[1]/li[2]/a[@href]',)), callback="parsef", follow= True),
        Rule (SgmlLinkExtractor(restrict_xpaths=('//*[@id="pagediv"]/ul/li/a[@href]',)), follow= True),
    )#//*[@id="pagediv"]/ul/li[3]/a
    #//*[@id="pagediv"]/ul/li[2]/a
    
    
    
    def parsef(self, response):
        hxs = Selector(response)
        titles = hxs.xpath("//div[@class='span6 push']")
        pric = hxs.xpath("//div[@class='span6 pull']")
        loc= hxs.xpath("//div[@class='page-title']")
        listid= hxs.xpath("//input[@id='hdncontentid']")
        
        items = []
        
        for listids in listid:
            item = PropertyItem()
            item['data_id'] =  map(unicode.strip, listids.xpath('@value').extract())
            item['management_by_landlord'] = 'None'
            item['areacode'] = 'None'
            item['mobile_lister'] = 'None'
            item['google_place_id'] = 'None'
            item['Possession'] = 'None'
            item['Launch_date'] = 'None'
            item['age'] = 'None'
            item['address'] = 'None'
            item['price_per_sqft'] = 'None'
            item['sublocality'] = 'None'
            item['lat'] = 0
            item['longt'] = 0
            item['Status'] = 'None'
            item['name_lister'] = 'None'
            item['Details'] = 'None'
            item['carpet_area'] = 'None'
        for locs in loc:
            
            item['platform']="Sulekha"
            item['city']="Mumbai"
            
            rentsale = map(unicode.strip, locs.xpath('//div[@class="pull-left"]/h1/text()[1]').extract())
            #print rentsale  
            #item['ptitle']= map(unicode.strip, locs.xpath('//div[@class="pull-left"]/h1/text()[1]').extract()) 
            if "Rent" in rentsale:
                item['txn_type'] = "Rent"
            if "Sale" or "sale" in rentsale:
                item['txn_type'] = "Sale"   
            local=map(unicode.strip, locs.xpath('//div[@class="pull-left"]/small/text()[2]').extract())
            locali=str(local).split(',')[0] 
            locali2= locali.split("'")[1]              
            item['locality'] = locali2
            #/html/body/div[6]/div[4]/div[1]/div[1]/div[1]/div/text()
            
            listdate= str(map(unicode.strip, locs.xpath('//div[@class="pull-left"]/small/text()[4]').extract()))
            b= listdate.split("on ")[1]
            #print "LDATE" + b
            b = b[:-2]
            b=b[1:]
            dates=str(datetime.strptime(b, '%b %d, %Y'))
            #print dates[5:7]+"/"+ dates[8:10]+"/"+dates[0:4]
            item['listing_date']= dates[5:7]+"/"+ dates[8:10]+"/"+dates[0:4]
            item['updated_date'] = item['listing_date']
            #struct_time = time.strptime(b, "%d %b %y")
            #print "returned tuple: %s " % struct_time
                     
        
        for titles in titles:       
            #item['property_type'] = "Residential"   
            #item['property_subtype'] = map(unicode.strip, titles.xpath('//ul/li[1]/span[2]/text()').extract())
            if "cial" in str(map(unicode.strip, titles.xpath('//ul/li[1]/span[2]/text()').extract())):
                item['property_type']="Commercial"
                c=0
            else:
                item['property_type']="Residential"
                c=1
            #item['configtype'] = map(unicode.strip, titles.xpath('//ul/li[2]/span[2]/text()').extract()) 
            
            if c==1:
                ctype=map(unicode.strip, titles.xpath('//ul/li[2]/span[2]/text()').extract()) 
                ct=str(ctype)
                #print "CT IS"+ ct
                if "HK" in ct or "RK" in ct  :
                    item['config_type'] = map(unicode.strip, titles.xpath('//ul/li[2]/span[2]/text()').extract())
                    
                else:
                    item['config_type'] = map(unicode.strip, titles.xpath('//ul/li[3]/span[2]/text()').extract())
                    
                
            try :
                if "uild" in str(titles.xpath('//ul/li[2]/span[1]/text()').extract()).split(',')[2]:
                    item['Building_name'] = map(unicode.strip, titles.xpath('//ul/li[2]/span[2]/text()').extract())
                else:
                    item['Building_name'] = 'None'  
            except IndexError:
                print "IndexErrrror"
               
                
            try:
                if "uild" in str(titles.xpath('//ul/li[3]/span[1]/text()').extract()).split(',')[2]:
                    item['Building_name'] = map(unicode.strip, titles.xpath('//ul/li[3]/span[2]/text()').extract()) 
                else:
                    item['Building_name'] = 'None'    
            except IndexError:
                    print "IndexErrrror"
                    
            try:
                if "uild" in str(titles.xpath('//ul/li[4]/span[1]/text()').extract()).split(',')[2]:
                    item['Building_name'] = map(unicode.strip, titles.xpath('//ul/li[4]/span[2]/text()').extract())
                else:
                    item['Building_name'] = 'None'    
            except IndexError:
                    print "IndexErrrror"
                    
            try:
                if "uild" in str(titles.xpath('//ul/li[5]/span[1]/text()').extract()).split(',')[2]:
                    item['Building_name'] = map(unicode.strip, titles.xpath('//ul/li[5]/span[2]/text()').extract())
                else:
                    item['Building_name'] = 'None'    
            except IndexError:
                    print "IndexErrrror"
                    
            try:
                if "uild" in str(titles.xpath('//ul/li[6]/span[1]/text()').extract()).split(',')[2]:
                    item['Building_name'] = map(unicode.strip, titles.xpath('//ul/li[6]/span[2]/text()').extract())
                else:
                    item['Building_name'] = 'None'   
            except IndexError:
                    print "IndexErrrror"
                    
            try:
                if "uild" in str(titles.xpath('//ul/li[7]/span[1]/text()').extract()).split(',')[2]:
                    item['Building_name'] = map(unicode.strip, titles.xpath('//ul/li[7]/span[2]/text()').extract())
                else:
                    item['Building_name'] = 'None'    
            except IndexError:
                    print "IndexErrrror"
                    
            try:
                if "uild" in str(titles.xpath('//ul/li[8]/span[1]/text()').extract()).split(',')[2]:
                    item['Building_name'] = map(unicode.strip, titles.xpath('//ul/li[8]/span[2]/text()').extract())
                else:
                    item['Building_name'] = 'None'    
            except IndexError:
                    print "IndexErrrror"
                    
                                                            
        for prices in pric:
            price = prices.xpath('//span[@class="price-green22"]/text()[2]').extract_first()
            if 'lakhs' in price:
                price=float(price.split(' ')[0])*100000
                #print price
                item['Selling_price']=str(price)
               
            elif 'crores' in price:
                price=float(price.split(' ')[0])*10000000
                item['Selling_price']=str(price)
                
            item['Monthly_Rent'] = '0'
            item['price_on_req'] = 'false'
            #item['Selling_Price'] = map(unicode.strip, prices.xpath('//span[@class="price-green22"]/text()[2]').extract())
            sq= str(map(unicode.strip, prices.xpath('//div[@class="page-details-info"]/b/text()').extract()))
            item['listing_by']=map(unicode.strip, prices.xpath('//div[@class="page-details-info"]/text()[2]').extract())
            
            #/html/body/div[6]/div[4]/div[1]/div[1]/div[1]/div/text()
            sqf= sq.split('\\x',1)
            sqq=sqf[0]
            ab=sqq.split("'")[1]
            #print sqq
            item['Bua_sqft']= ab
            
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
            items.append(item)
        return(items)
    
    

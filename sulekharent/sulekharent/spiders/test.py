from scrapy.spiders import BaseSpider
from scrapy.selector import Selector
from sulekharent.items import PropertyItem
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors.sgml import SgmlLinkExtractor
import urlparse
from datetime import datetime

class MySpider(CrawlSpider):
    
    name = "SulekhaRentSpider"
    
    allowed_domains = ['property.sulekha.com']
    start_urls = ["http://property.sulekha.com/property-for-rent/mumbai",
   ]
    rules = (
        Rule(SgmlLinkExtractor(allow=('property.sulekha.com'), restrict_xpaths=('//*[@id="listings-wrap"]/li/div[1]/div/strong/a[@href]',)), callback="parsef", follow= True),
        Rule (SgmlLinkExtractor(restrict_xpaths=('//*[@id="pagediv"]/ul/li/a[@href]',)), follow= True),
    )
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
                    
        for locs in loc:
            fl=0
            item['platform']="Sulekha"
            item['lat'] = 0
            item['longt'] = 0
            item['city']="Mumbai"
            item['Details'] = 'None'
            item['carpet_area'] = 'None'
            item['Status'] = 'None'
            item['sublocality'] = 'None'
            item['age'] = 'None'
            item['google_place_id'] = 'None'
            item['Possession'] = 'None'
            item['Launch_date'] = 'None'
            item['price_per_sqft'] = 'None'
            item['mobile_lister'] = 'None'
            item['areacode'] = 'None'
            item['management_by_landlord'] = 'None'
            
            item['txn_type'] = "Rent"
            item['address']= map(unicode.strip, locs.xpath('//div[@class="page-title"]/span/small/text()[2]').extract())
            local=map(unicode.strip, locs.xpath('//div[@class="page-title"]/span/small/text()[2]').extract())   
            if str(map(unicode.strip, locs.xpath('//div[@class="page-title"]/span/small/text()[2]').extract())).count(',')==1:
                fl=1               
                locali=str(local).split(',')[0] 
                locali2= locali.split("'")[1]              
                item['locality'] = locali2
                
               
            local1 = str(local).split(",")[0]
            local1=local1.replace("'","")
            local1=local1.replace("[","")
            local1=local1.replace("]","")
            local1=local1.replace("u","")
            item['Building_name']= local1
            if item['Building_name'] == '':
                item['Building_name'] = 'None'
            
            if "Posted" in str(map(unicode.strip, locs.xpath('//div[@class="page-title"]/span/small/text()[1]').extract())):
                ld = str(map(unicode.strip, locs.xpath('//div[@class="page-title"]/span/small/text()[1]').extract()))
            elif "Posted" in str(map(unicode.strip, locs.xpath('//div[@class="page-title"]/span/small/text()[2]').extract())):
                ld = str(map(unicode.strip, locs.xpath('//div[@class="page-title"]/span/small/text()[2]').extract()))
            elif "Posted" in str(map(unicode.strip, locs.xpath('//div[@class="page-title"]/span/small/text()[3]').extract())):
                ld = str(map(unicode.strip, locs.xpath('//div[@class="page-title"]/span/small/text()[3]').extract()))
            b= ld.split("on ")[1]
            
            b = b[:-2]
            b=b[0:]
            dates=str(datetime.strptime(b, '%b %d, %Y'))
            item['listing_date']= dates[5:7]+"/"+ dates[8:10]+"/"+dates[0:4]   
            item['updated_date'] = item['listing_date']
            
        for titles in titles:              
            #item['property_subtype'] = map(unicode.strip, titles.xpath('//ul/li[1]/span[2]/text()').extract())
            c=0
            if "cial" in str(map(unicode.strip, titles.xpath('//ul/li[1]/span[2]/text()').extract())):
                item['property_type']="Commercial"
                item['config_type'] = 'None'
                  
            elif "rial" in str(map(unicode.strip, titles.xpath('//ul/li[1]/span[2]/text()').extract())) :
                item['property_type']="Industrial"
                item['config_type'] = 'None'
            else:
                item['property_type']="Residential"
                c=1
            
             
            if c==1:
                ctype=map(unicode.strip, titles.xpath('//ul/li[2]/span[2]/text()').extract()) 
                ct=str(ctype)
                #print "CT IS"+ ct
                if "HK" in ct or "RK" in ct  :
                    item['config_type'] = map(unicode.strip, titles.xpath('//ul/li[2]/span[2]/text()').extract())
                    #print  str(titles.xpath('//ul/li[2]/span[2]/text()').extract()).split()[1:3]                   
                else:
                    item['config_type'] = 'None'#map(unicode.strip, titles.xpath('//ul/li[3]/span[2]/text()').extract())
                    
                    
            try :
                if "uild" in str(titles.xpath('//ul/li[2]/span[1]/text()').extract()):
                    item['Building_name'] = map(unicode.strip, titles.xpath('//ul/li[2]/span[2]/text()').extract()) 
       
            except IndexError:
                print "IndexErrrror"
                #/html/body/div[4]/div[4]/div[1]/div[1]/div[2]/ul/li[6]/span[1]
            try:
                if "uild" in str(titles.xpath('//ul/li[3]/span[1]/text()').extract()):
                    item['Building_name'] = map(unicode.strip, titles.xpath('//ul/li[3]/span[2]/text()').extract()) 
                    
            except IndexError:
                    print "IndexErrrror"
            try:
                if "uild" in str(titles.xpath('//ul/li[4]/span[1]/text()').extract()):
                    item['Building_name'] = map(unicode.strip, titles.xpath('//ul/li[4]/span[2]/text()').extract())
                    
            except IndexError:
                    print "IndexErrrror"
            try:
                if "uild" in str(titles.xpath('//ul/li[5]/span[1]/text()').extract()):
                    item['Building_name'] = map(unicode.strip, titles.xpath('//ul/li[5]/span[2]/text()').extract())
                    
            except IndexError:
                    print "IndexErrrror"
            try:
                if "uild" in str(titles.xpath('//ul/li[6]/span[1]/text()').extract()):
                    item['Building_name'] = map(unicode.strip, titles.xpath('//ul/li[6]/span[2]/text()').extract())
                    
                    #/html/body/div[4]/div[4]/div[1]/div[1]/div[2]/ul/li[6]/span[1]
            except IndexError:
                    print "IndexErrrror"
            try:
                if "uild" in str(titles.xpath('//ul/li[7]/span[1]/text()').extract()):
                    item['Building_name'] = map(unicode.strip, titles.xpath('//ul/li[7]/span[2]/text()').extract())
                    
            except IndexError:
                    print "IndexErrrror"
            try:
                if "uild" in str(titles.xpath('//ul/li[8]/span[1]/text()').extract()):
                    item['Building_name'] = map(unicode.strip, titles.xpath('//ul/li[8]/span[2]/text()').extract())
                    
            except IndexError:
                    print "IndexErrrror"
            if fl!=1:
                try:
                    if "ocation" in str(titles.xpath('//ul/li[2]/span[1]/text()').extract()):
                        item['locality'] = map(unicode.strip, titles.xpath('//ul/li[2]/span[2]/text()').extract())
                    
                    
                except IndexError:
                    print "IndexErrrror"
                try:
                    if "ocation" in str(titles.xpath('//ul/li[3]/span[1]/text()').extract()):
                        item['locality'] = map(unicode.strip, titles.xpath('//ul/li[3]/span[2]/text()').extract()) 
                    
                    
                except IndexError:
                    print "IndexErrrror"
                try:
                    if "ocation" in str(titles.xpath('//ul/li[4]/span[1]/text()').extract()):
                        item['locality'] = map(unicode.strip, titles.xpath('//ul/li[4]/span[2]/text()').extract())
                               
                except IndexError:
                    print "IndexErrrror"
                try:
                    if "ocation" in str(titles.xpath('//ul/li[5]/span[1]/text()').extract()):
                         item['locality'] = map(unicode.strip, titles.xpath('//ul/li[5]/span[2]/text()').extract())
                except IndexError:
                    print "IndexErrrror"
                try:
                    if "ocation" in str(titles.xpath('//ul/li[6]/span[1]/text()').extract()):
                        item['locality'] = map(unicode.strip, titles.xpath('//ul/li[6]/span[2]/text()').extract())
                except IndexError:
                    print "IndexErrrror"
                    

                try:
                    if "ocation" in str(titles.xpath('//ul/li[7]/span[1]/text()').extract()):
                        item['locality'] = map(unicode.strip, titles.xpath('//ul/li[7]/span[2]/text()').extract())
                    
                except IndexError:
                    print "IndexErrrror"
                try:
                    if "ocation" in str(titles.xpath('//ul/li[8]/span[1]/text()').extract()):
                        item['locality'] = map(unicode.strip, titles.xpath('//ul/li[8]/span[2]/text()').extract())
                    
                except IndexError:
                    print "IndexErrrror"
            
            #print item['locality']                                                
        for prices in pric:
            
            mr=str(map(unicode.strip, prices.xpath('//span[@class="price-green22"]/text()[2]').extract()))
          
            mr1=mr[2:10]
            mr1=mr1.replace("'","")
            mr1=mr1.replace("[","")
            mr1=mr1.replace("]","")
            mr1=mr1.replace("u","")
            mr1=mr1.replace(",","")
            
            if 'lakhs'  in mr1:
                price=str(float(mr1.split("lakhs")[0])*100000)
            elif 'la' in mr1:
                price=str(float(mr1.split("la")[0])*100000)
            elif 'lak' in mr1:
                price=str(float(mr1.split("lak")[0])*100000)
            elif 'lakh' in mr1:
                price=str(float(mr1.split("lakh")[0])*100000)
                #item['Monthly_Rent']=float(mr1.split())
            elif 'cr' in mr1:
                price=str(float(mr1.split("cr")[0])*10000000)
            else:
                price = mr1
            item['Monthly_Rent']=str(price)
            if item['Monthly_Rent'] == '':
                item['Monthly_Rent'] = '0'
            item['Selling_price'] = '0'
            if item['Selling_price'] == '0' and item['Monthly_Rent'] == '0':
                item['price_on_req'] = 'true'
            else:
                item['price_on_req'] = 'false'
                #if len(mr1)<=4:
                    #item['Monthly_Rent']=""
                
            
            item['name_lister']=map(unicode.strip, prices.xpath('//div[@class="page-details-info"]/text()[2]').extract())
            item['listing_by']= str(map(unicode.strip, prices.xpath('//div[@class="page-details-info"]/i[2]/text()').extract())).replace("[","").replace("]","").replace("'","").replace("(","").replace(")","").replace("u","")
            
            #if not 'K' in item['config_type']:
             #   item['config_type'] = 'None'
            #item['listing_by']=map(unicode.strip, prices.xpath('//div[@class="page-details-info"]/text()[2]').extract())                        
            sq= str(map(unicode.strip, prices.xpath('//div[@class="page-details-info"]/b/text()').extract()))
            sqf= sq.split('\\x',1)
            sqq=sqf[0]
            ab=sqq.split("S")[0]
            #print ab
            try:
                item['Bua_sqft']= ab.split("'")[1]
                if 'l' in ab.split("'")[1]:
                    item['Bua_sqft']=0
                
            except:
                print "IndexErrrror"
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
    

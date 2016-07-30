import scrapy
from magicbrickrent.items import MagicbrickrentItem
from scrapy.spiders import Spider
from scrapy.spiders import CrawlSpider, Rule
from scrapy.selector import Selector
from scrapy.http import Request
from scrapy.http import FormRequest
from urlparse import urljoin
from datetime import datetime as dt
from datetime import time,timedelta
from datetime import date
import time

class MagicrentSpider(scrapy.Spider):
    name = 'magicrentSpider'
    
    
    allowed_domains = ['magicbricks.com']
    start_urls = ['http://www.magicbricks.com/property-for-rent/residential-real-estate?proptype=Multistorey-Apartment,Builder-Floor-Apartment,Penthouse,Studio-Apartment,Service-Apartment,Residential-House,Villa&cityName=Mumbai/Page-1']
    custom_settings = {
            'DEPTH_LIMIT' : 10000,
	        'DOWNLOAD_DELAY': 4
	    }
	    
    #def __init__(self, category=None):
        #self.url_rem = []
    
    def parse(self,response):
        #handle = [ 301 , 401 , 403 , 404 , 408 , 429 , 503 ]
        #if response.status in handle:
        #    time.sleep(300)
        #    url = response.url
        #    yield Request(url,callback=self.parse)
            #self.url_rem.append(response.url)
            #curPage=int(response.url.split("-")[-1])
            #next_url = 'http://www.magicbricks.com/property-for-rent/residential-real-estate?proptype=Multistorey-Apartment,Builder-Floor-Apartment,Penthouse,Studio-Apartment,Service-Apartment,Residential-House,Villa&cityName=Mumbai/Page-' + str(curPage+1)
            #yield Request(next_url, callback=self.parse)
        #else:
            hxs = Selector(response)
            
            data = hxs.xpath('//div[@class="srpColm2"]/div[@class="proColmleft"]')
            lister = hxs.xpath('//div[@class="srpColm2"]')
            dates = hxs.xpath('//span[@class="postedBy"]')
        
            for i in data:
                item = MagicbrickrentItem()
            
                item['platform'] = 'Magicbrick'
                item['txn_type'] = 'Rent'
                item['property_type'] = 'Residential'
                item['city'] = 'Mumbai'
                item['data_id'] = i.xpath('div[1]/div[1]/@onclick').extract_first().split("'")[5]
                item['lat'] = i.xpath('div[1]/div[1]/div[1]/div[2]/span/a/@onclick').extract_first().split('&')[0].split("?")[-1].split("=")[-1]
                if item['lat'] == '':
                    item['lat'] = 0
                item['longt'] = i.xpath('div[1]/div[1]/div[1]/div[2]/span/a/@onclick').extract_first().split('&')[1].split("=")[-1]
                if item['longt'] == '':
                    item['longt'] = 0
                item['locality'] = i.xpath('div[1]/div[1]/div[1]/div[2]/p/a/span[1]/span/text()').extract_first()
                item['Building_name'] = i.xpath('div[1]/div[1]/div[1]/div[2]/p/a/span[1]/text()').extract_first().replace("in","").replace("\n","")
                if item['Building_name'] == '':
                    item['Building_name'] = 'None'
                item['config_type'] = i.xpath('div[1]/div[1]/div[1]/div[2]/p/a/strong/text()').extract_first()[:5]
                item['Selling_price'] = '0'
                price = i.xpath('div[1]/div[1]/div[1]/div[1]/div[1]/div/span/text()').extract_first()
                if 'Lac' in price:
                    price = float(price.replace("Lac",""))*100000
                    item['Monthly_Rent'] = str(price)
                else:
                    price = price.replace(",","")
                    item['Monthly_Rent'] = str(float(price))
                if item['Selling_price'] == '0' and item['Monthly_Rent'] == '0':
                    item['price_on_req'] = 'true'
                else:
                    item['price_on_req'] = 'false'
                item['price_per_sqft'] = 'None'
                item['carpet_area'] = 'None'
                item['address'] = 'None'
                item['sublocality'] = 'None'
                item['age'] = 'None'
                item['google_place_id'] = 'None'
                item['Launch_date'] = 'None'
                item['Possession'] = 'None'
                item['mobile_lister'] = 'None'
                item['areacode'] = 'None'
                item['management_by_landlord'] = 'None'
                item['listing_by'] = lister.xpath('div[5]/div[3]/ul/li[3]/div/div[1]/div/div[1]/text()').extract_first()
                item['name_lister'] = str(str(lister.xpath('div[5]/div[3]/ul/li[3]/div/div[3]/text()').extract_first()).replace("\n",""))
                check = i.xpath('div[2]/div[1]/label/text()').extract_first()
                if check == 'Details':
                    item['Bua_sqft'] = i.xpath('div[2]/div[1]/ul/li[1]/span/text()').extract_first().split()[0]
                else:
                    item['Bua_sqft'] = ''
                item['Status'] = i.xpath('div[2]/div[2]/text()').extract()[1:]
                item['Details'] = str(i.xpath('div[2]/div[1]/ul/li[2]/text()').extract_first())+' '+str(i.xpath('div[2]/div[1]/ul/li[3]/text()').extract_first())+' '+str(i.xpath('div[2]/div[1]/ul/li[4]/text()').extract_first())+' '+str(i.xpath('div[2]/div[1]/ul/li[5]/text()').extract_first())
            
                day = dates.xpath('text()').extract_first()
                day = day.replace("Posted: ","").replace("Posted ","")
            
                if 'Today' in day:
                    item['listing_date'] = str(date.today().month)+'/'+str(date.today().day)+'/'+str(date.today().year) + ' 00:00:00'
                elif 'Yesterday' in day:
                    item['listing_date'] = str((date.today() - timedelta(days=1)).month)+"/"+str((date.today() - timedelta(days=1)).day)+"/"+str((date.today() - timedelta(days=1)).year) + ' 00:00:00'
                elif 'th' in day:
                    day = day.replace("th","")
                    day = dt.strftime(dt.strptime(day,'%d %b'),'%m/%d')+'/'+str(date.today().year) + ' 00:00:00'
                    item['listing_date'] = day
                elif 'st' in day:
                    day = day.replace("st","")
                    day = dt.strftime(dt.strptime(day,'%d %b'),'%m/%d')+'/'+str(date.today().year) + ' 00:00:00'
                    item['listing_date'] = day
                elif 'rd' in day:
                    day = day.replace("rd","")
                    day = dt.strftime(dt.strptime(day,'%d %b'),'%m/%d')+'/'+str(date.today().year) + ' 00:00:00'
                    item['listing_date'] = day
                elif 'nd' in day:
                    day = day.replace("nd","")
                    day = dt.strftime(dt.strptime(day,'%d %b'),'%m/%d')+'/'+str(date.today().year) + ' 00:00:00'
                    item['listing_date'] = day
                item['updated_date'] = item['listing_date']

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
        
            curPage=int(response.url.split("-")[-1])    
            #print curPage
            try:
                maxPage = int(hxs.xpath('//div[@id="pagination"]/span/a[last()]/@href').extract_first().split('-')[-1])
            except:
                try:
                    maxPage = int(hxs.xpath('//div[@id="pagination"]/span/a[@class="act selected"]/text()').extract_first()) + 1
                except:
                    maxPage = curPage + 1
            #print maxPage
        
            if curPage <= maxPage :
                nextPage = curPage+1
                next_url = 'http://www.magicbricks.com/property-for-rent/residential-real-estate?proptype=Multistorey-Apartment,Builder-Floor-Apartment,Penthouse,Studio-Apartment,Service-Apartment,Residential-House,Villa&cityName=Mumbai/Page-' + str(nextPage)
                yield Request(next_url, callback=self.parse)
            
            
            
    
    

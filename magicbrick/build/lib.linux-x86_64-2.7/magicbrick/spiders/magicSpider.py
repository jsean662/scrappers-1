import scrapy
from magicbrick.items import MagicbrickItem
from scrapy.spiders import Spider
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.selector import Selector
from scrapy.http import Request
from urlparse import urljoin
from datetime import datetime as dt
from datetime import time,timedelta
from datetime import date
import time

class MagicSpider(scrapy.Spider):
    name = 'magicSpider'
    allowed_domains = ['magicbricks.com']
    start_urls = ['http://www.magicbricks.com/property-for-sale/residential-real-estate?proptype=Multistorey-Apartment,Builder-Floor-Apartment,Penthouse,Studio-Apartment,Residential-House,Villa&cityName=Mumbai/Page-1']
    rules = (Rule(LinkExtractor(deny=(), allow=('http://www.magicbricks.com/'), ), callback='parse', follow=True, ),)
    custom_settings = {
            'DEPTH_LIMIT' : 6000,
	        'DOWNLOAD_DELAY': 5
	    }
      
    def parse(self,response):
        #handle = [ 301 , 401 , 403 , 404 , 408 , 429 , 503 ]
        #if response.status in handle:
        #    time.sleep(600)
        #    url = response.url
        #    yield Request(url,callback=self.parse)
        #else:
            #print response.status,type(response.status)
            hxs = Selector(response)
            #maxNo = int(str(hxs.xpath('//div[@class="srpHdrComLeft"]/h1/text()').extract()).split(" ")[0].replace("[","").replace("u","").replace("'",""))
            #print maxNo
            data = hxs.xpath('//div[@class="srpColm2"]')
            #print data
            dates = hxs.xpath('//div[@class="postedBy"]')
            for i in data:
                item = MagicbrickItem()
            
                item['Building_name'] = i.xpath('div[@class="proColmleft"]/div[1]/div/p/a/abbr/span[1]/text()').extract_first().replace("in","").replace("The Address","").replace("\n","")
                if item['Building_name'] == '':
                    item['Building_name'] = 'None'
                item['lat'] = i.xpath('div[@class="proColmleft"]/div[1]/div[1]/span/span[2]/@onclick').extract_first().split('&')[0].split('?')[-1].split("=")[-1]
                if item['lat'] == '':
                    item['lat'] = 0
                item['longt'] = i.xpath('div[@class="proColmleft"]/div[1]/div[1]/span/span[2]/@onclick').extract_first().split('&')[1].split("=")[-1]
                if item['longt'] == '':
                    item['longt'] = 0
                item['platform'] = 'magicbricks'
                item['carpet_area'] = 'None'
                item['data_id'] = i.xpath('div[@class="proColmleft"]/div[1]/div[1]/@onclick').extract_first().split("'")[5]
                item['config_type'] = i.xpath('div[@class="proColmleft"]/div[1]/div/p/a/strong/text()').extract_first()[:6]
                if not 'K' in item['config_type']:
                    item['config_type'] = 'None'
                item['Bua_sqft'] = i.xpath('div[@class="proColmleft"]/div[1]/div/p/a/span/text()').extract()[0].split()[0]
                item['city'] = 'Mumbai'
                item['locality'] = i.xpath('div[@class="proColmleft"]/div[1]/div/p/a/abbr/span[1]/span/text()').extract_first()
                status = response.xpath('//label/text()').extract_first()
                if status=='Status':
                    item['Status'] = i.xpath('div[@class="proColmleft"]/div[2]/div[1]/text()').extract()[1:]
                    item['Details'] = str(i.xpath('div[@class="proColmleft"]/div[2]/div[2]/ul/text()').extract_first())+' '+str(i.xpath('div[@class="proColmleft"]/div[2]/div[2]/ul/li[1]/text()').extract_first())+' '+str(i.xpath('div[@class="proColmleft"]/div[2]/div[2]/ul/li[2]/text()').extract_first())+' '+str(i.xpath('div[@class="proColmleft"]/div[2]/div[2]/ul/li[3]/text()').extract_first())+' '+str(i.xpath('div[@class="proColmleft"]/div[2]/div[2]/ul/li[4]/text()').extract_first())
                elif status=='Builder':
                    item['Status'] = i.xpath('div[@class="proColmleft"]/div[2]/div[2]/text()').extract()[1:]
                    item['Details'] = str(i.xpath('div[@class="proColmleft"]/div[2]/div[3]/ul/text()').extract_first())+' '+str(i.xpath('div[@class="proColmleft"]/div[2]/div[3]/ul/li[1]/text()').extract_first())+' '+str(i.xpath('div[@class="proColmleft"]/div[2]/div[3]/ul/li[2]/text()').extract_first())+' '+str(i.xpath('div[@class="proColmleft"]/div[2]/div[3]/ul/li[3]/text()').extract_first())+' '+str(i.xpath('div[@class="proColmleft"]/div[2]/div[3]/ul/li[4]/text()').extract_first())
                price = i.xpath('div[@class="proColmRight"]/div/div/div/span/text()').extract_first()
                if 'Lac' in price:
                    item['Selling_price']=str(float(price.split()[0])*100000)
                elif 'Cr' in price:
                    item['Selling_price']=str(float(price.split()[0])*10000000)
                else:
                    item['Selling_price'] = '0'
                if item['Selling_price'] == 'None':
                    item['Selling_price'] = '0'
                item['Monthly_Rent'] = '0'
                if item['Selling_price'] == '0' and item['Monthly_Rent'] == '0':
                    item['price_on_req'] = 'true'
                else:
                    item['price_on_req'] = 'false'

                try:
                    item['price_per_sqft'] = i.xpath('div[@class="proColmRight"]/div[@class="proPriceColm2"]/div[@class="proPriceColm2"]/div[@class="sqrPrice"]/span[@class="sqrPriceField"]/text()').extract_first().split()[0].replace(",","")
                except:
                    item['price_per_sqft'] = '0'
                item['listing_by'] = i.xpath('div[@class="proBtnRow"]/div[3]/ul/li[@class="agentDeatilsBox"]/div/div[1]/div/div[1]/text()').extract_first()
                item['name_lister'] = i.xpath('div[@class="proBtnRow"]/div[3]/ul/li[@class="agentDeatilsBox"]/div/div[3]/text()').extract_first()
                item['property_type'] = 'Residential'
                item['txn_type'] = 'sale'
                item['name_lister'] = 'None'
                item['address'] = 'None'
                item['sublocality'] = 'None'
                item['age'] = 'None'
                item['google_place_id'] = 'None'
                item['Possession'] = 'None'
                item['Launch_date'] = 'None'
                item['mobile_lister'] = 'None'
                item['areacode'] = 'None'
                item['management_by_landlord'] = 'None'
                
                day = dates.xpath('text()').extract_first()
                day = day.replace("Posted: ","").replace("Posted ","")
            
                if 'Today' in day:
                    item['listing_date'] = str(date.today().month)+'/'+str(date.today().day)+'/'+str(date.today().year)
                elif 'Yesterday' in day:
                    item['listing_date'] = str((date.today() - timedelta(days=1)).month)+"/"+str((date.today() - timedelta(days=1)).day)+"/"+str((date.today() - timedelta(days=1)).year)
                elif 'th' in day:
                    day = day.replace("th","")
                    day = dt.strftime(dt.strptime(day,'%d %b'),'%m/%d')+'/'+str(date.today().year)
                    item['listing_date'] = day
                elif 'st' in day:
                    day = day.replace("st","")
                    day = dt.strftime(dt.strptime(day,'%d %b'),'%m/%d')+'/'+str(date.today().year)
                    item['listing_date'] = day
                elif 'rd' in day:
                    day = day.replace("rd","")
                    day = dt.strftime(dt.strptime(day,'%d %b'),'%m/%d')+'/'+str(date.today().year)
                    item['listing_date'] = day
                elif 'nd' in day:
                    day = day.replace("nd","")
                    day = dt.strftime(dt.strptime(day,'%d %b'),'%m/%d')+'/'+str(date.today().year)
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
        
        #   for i in date:
        #        item['listing_date'] = i.xpath('text()').extract_first().split()[1:]
                #yield item
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
                nextPage=curPage+1
                #print curPage,maxPage,nextPage
                next_url = 'http://www.magicbricks.com/property-for-sale/residential-real-estate?proptype=Multistorey-Apartment,Builder-Floor-Apartment,Penthouse,Studio-Apartment,Residential-House,Villa&cityName=Mumbai/Page-' + str(nextPage)
                yield Request(next_url, callback=self.parse)
                #print nextPage,next_url'''

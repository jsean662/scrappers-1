import scrapy
import sys
import logging
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
    #http://www.magicbricks.com/property-for-rent/residential-real-estate?proptype=Multistorey-Apartment,Builder-Floor-Apartment,Penthouse,Studio-Apartment,Service-Apartment,Residential-House,Villa&cityName=Navi-Mumbai/Page-1
    custom_settings = {
            'DEPTH_LIMIT' : 10000,
	        'DOWNLOAD_DELAY': 4
	    }
	    
    #def __init__(self, category=None):
        #self.url_rem = []
    
    def parse(self,response):
            hxs = Selector(response)
            #print response.body
            data = hxs.xpath('//div[@class="srpColm2"]')
            #print data
            #lister = hxs.xpath('//div[@class="srpColm2"]')
            #dates = hxs.xpath('//span[@class="postedBy"]')
        
            for i in data:
                item = MagicbrickrentItem()
            
                item['platform'] = 'Magicbrick'
                item['txn_type'] = 'Rent'
                item['property_type'] = 'Residential'
                item['city'] = 'Mumbai'
                try:
                    item['data_id'] = i.xpath('div[@class="minHeightBlock"]/div[@class="proColmleft"]/div[@class="proNameWrap "]/div[@class="proNameColm1"]/@onclick').extract_first().split("'")[5]
                except:
                    print i.xpath('div[@class="minHeightBlock"]/div[@class="proColmleft"]/div[@class="proNameWrap "]/div[@class="proNameColm1"]/@onclick').extract_first()
                    item['data_id'] = 'None'
                
                item['lat'] = i.xpath('div[@class="minHeightBlock"]/div[@class="proColmleft"]/div[@class="proNameWrap "]/div[@class="proNameColm1"]/div[@class="srpTopDetailWrapper"]/div[@class="srpAnchor"]/span[@class="seeOnMapLink seeOnMapLinkRent"]/a/@onclick').extract_first().split('&')[0].split("?")[-1].split("=")[-1]
                if item['lat'] == '':
                    item['lat'] = 0
                
                item['longt'] = i.xpath('div[@class="minHeightBlock"]/div[@class="proColmleft"]/div[@class="proNameWrap "]/div[@class="proNameColm1"]/div[@class="srpTopDetailWrapper"]/div[@class="srpAnchor"]/span[@class="seeOnMapLink seeOnMapLinkRent"]/a/@onclick').extract_first().split('&')[1].split("=")[-1]
                if item['longt'] == '':
                    item['longt'] = 0
                
                item['locality'] = i.xpath('div[@class="minHeightBlock"]/div[@class="proColmleft"]/div[@class="proNameWrap "]/div[@class="proNameColm1"]/div[@class="srpTopDetailWrapper"]/div[@class="srpAnchor"]/p[@class="proHeading"]/a/span[@class="maxProDesWrap showNonCurtailed"]/span[@class="localityFirst"]/text()').extract_first()
                
                item['Building_name'] = i.xpath('div[@class="minHeightBlock"]/div[@class="proColmleft"]/div[@class="proNameWrap "]/div[@class="proNameColm1"]/div[@class="srpTopDetailWrapper"]/div[@class="srpAnchor"]/p[@class="proHeading"]/a/span[@class="maxProDesWrap showNonCurtailed"]/text()').extract_first().replace("in","").replace("\n","")
                if item['Building_name'] == '':
                    item['Building_name'] = 'None'
                elif 'rent' in item['Building_name']:
                    item['Building_name'] = 'None'
                
                item['config_type'] = i.xpath('div[@class="minHeightBlock"]/div[@class="proColmleft"]/div[@class="proNameWrap "]/div[@class="proNameColm1"]/div[@class="srpTopDetailWrapper"]/div[@class="srpAnchor"]/p[@class="proHeading"]/a/@href').extract_first().split('/')[-1].split('-')[:2]
                
                item['Selling_price'] = '0'
                
                price = i.xpath('div[@class="minHeightBlock"]/div[@class="proColmleft"]/div[@class="proNameWrap "]/div[@class="proNameColm1"]/div[@class="srpTopDetailWrapper"]/div[@class="srpPriceWrap newPriceBlock"]/div[@class="proPriceColm2"]/div[@class="proPrice"]/span[@class="proPriceField"]/text()').extract_first()
                if price==None:
                    item['Monthly_Rent'] = '0'
                    item['price_on_req'] = 'true'
                elif 'Lac' in price:
                    price = float(price.replace("Lac",""))*100000
                    item['Monthly_Rent'] = str(price)
                elif 'Cr' in price:
                    price = float(price.replace(" Cr",""))*10000000
                    item['Monthly_Rent'] = str(price)
                else:
                    price = price.replace(",","")
                    item['Monthly_Rent'] = str(float(price))
                # except:
                #     price = i.xpath('div[@class="minHeightBlock"]/div[@class="proColmleft"]/div[@class="proNameWrap "]/div[@class="proNameColm1"]/div[@class="srpTopDetailWrapper"]/div[@class="srpPriceWrap newPriceBlock"]/div[@class="proPriceColm2"]/div[@class="proPrice"]/span[2]/a/text()').extract_first()
                #     if 'Call ' in price:
                #         item['Monthly_Rent'] = '0'
                #         item['price_on_req'] = 'true'
                
                if item['Selling_price'] == '0' and item['Monthly_Rent'] == '0':
                    item['price_on_req'] = 'true'
                else:
                    item['price_on_req'] = 'false'
                
                item['price_per_sqft'] = 0
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
                
                item['listing_by'] = i.xpath('div[@class="proBtnRow"]/div[@class="srpBlockLeftBtn"]/ul/li[@class="agentDeatilsBox"]/div[@class="proAgentWrap"]/div[@class="iconAgentSmartCont"]/div[@class="proAgent"]/div[1]/text()').extract_first()
                
                item['name_lister'] = i.xpath('div[@class="proBtnRow"]/div[@class="srpBlockLeftBtn"]/ul/li[@class="agentDeatilsBox"]/div[@class="proAgentWrap"]/div[@class="comNameElip"]/text()').extract_first().replace('\n','')
                
                item['Bua_sqft'] = i.xpath('div[@class="minHeightBlock"]/div[@class="proColmleft"]/div[@class="proNameWrap "]/div[@class="proNameColm1"]/div[@class="srpTopDetailWrapper"]/div[@class="srpAnchor"]/p[@class="proHeading"]/a/@href').extract_first().split('/')[-1].split('-')[2]
                
                item['Status'] = str(i.xpath('div[@class="minHeightBlock"]/div[@class="proColmleft"]/div[@class="proDetailsRow proDetailsRowListing proDetailsRowRent"]/div[@class="proDetailsRowElm"]/text()').extract()).replace('[u','').replace(']','').replace(',',' ').replace(' u','').replace("'",'').replace('\\n','')
                
                item['Details'] = str(i.xpath('div[@class="minHeightBlock"]/div[@class="proColmleft"]/div[@class="proDetailsRow proDetailsRowListing proDetailsRowRent"]/div[@class="proDetailsRowElm"]/ul/li/text()').extract()).replace('[u','').replace(']','').replace(',',' ').replace(' u','').replace("'",'').replace('\\n','')
                
                day = i.xpath('div[@class="minHeightBlock"]/div[@class="proColmleft"]/div[@class="proNameWrap "]/div[@class="proNameColm1"]/div[@class="proRentPost"]/span[@class="postedBy"]/text()').extract_first()
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
                next_url = 'http://www.magicbricks.com/property-for-rent/residential-real-estate?proptype=Multistorey-Apartment,Builder-Floor-Apartment,Penthouse,Studio-Apartment,Service-Apartment,Residential-House,Villa&cityName=Navi-Mumbai/Page-' + str(nextPage)
                yield Request(next_url, callback=self.parse)
                
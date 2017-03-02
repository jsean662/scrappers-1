import scrapy
from scrapy import log
# from urlparse import urljoin
from scrapy.spiders import Spider
from scrapy.http import Request
from scrapy.exceptions import CloseSpider
from scrapy.spiders import CrawlSpider, Rule
from scrapy.selector import HtmlXPathSelector
from scrapy.http import Request
from scrapy.linkextractors import LinkExtractor
from scrapy.selector import Selector
from ..items import Website
from scrapy.loader import ItemLoader
import time
import unicodedata
import json
import time
import datetime
from datetime import datetime as dt
import re

class MakaanSpider(CrawlSpider):
    name = "makaanMumbai"
    
    allowed_domains = ['makaan.com']
    start_urls = [  
                   "https://www.makaan.com/listings?listingType=buy&pageType=LISTINGS_PROPERTY_URLS&cityName=Mumbai&cityId=18&templateId=MAKAAN_CITY_LISTING_BUY&page=1",
                   "https://www.makaan.com/listings?listingType=rent&pageType=CITY_URLS&cityName=Mumbai&cityId=18&templateId=MAKAAN_CITY_LISTING_BUY&page=1"
                ]
     
    item = Website()
    def parse(self, response):
        hxs = Selector(response)
        P = "//div[@class='cardholder']"
        a = hxs.xpath(P)
        
        for i in a:
            detail = i.xpath('div[@class="cardWrapper"]/script/text()').extract_first()
            data = json.loads(detail)

            self.item['age'] = 'None'
            self.item['Possession'] = '0'
            self.item['Details'] = 'None'
            self.item['carpet_area'] = '0'
            self.item['management_by_landlord'] = 'None'
            self.item['areacode'] = 'None'
            self.item['mobile_lister'] = 'None'
            self.item['google_place_id'] = 'None'
            self.item['Launch_date'] = '0'
            self.item['address'] = 'None'
            self.item['listing_by'] = 'None'
            self.item['sublocality'] = 'None'
            
            self.item['property_type'] = data['propertyType']

            self.item['platform'] = 'makaan'

            self.item['data_id'] = data['id']

            self.item['name_lister'] = data['builderName']
            if self.item['name_lister'] == '':
                self.item['name_lister'] = 'None'

            self.item['lat'] = data['latitude']
            if self.item['lat'] == '':
                self.item['lat'] = '0'

            self.item['longt'] = data['longitude']
            if self.item['longt'] == '':
                self.item['longt'] = '0'

            self.item['locality'] = data['localityName']

            self.item['city'] = data['cityName']

            self.item['Building_name'] = data['fullName']
            if self.item['Building_name'] == '':
                self.item['Building_name'] = 'None'

            self.item['config_type'] = data['bedrooms']+'BHK'

            self.item['txn_type'] = data['listingCategory']
            if 'mary' in self.item['txn_type']:
                self.item['txn_type'] = 'Sale'

            if 'ale' in self.item['txn_type']:
                self.item['Selling_price'] = data['price']
                self.item['Monthly_Rent'] = '0'
            if 'ntal' in self.item['txn_type']:
                self.item['Monthly_Rent'] = data['price']
                self.item['Selling_price'] = '0'

            if self.item['Selling_price'] == '0' and self.item['Monthly_Rent'] == '0':
                self.item['price_on_req'] = 'true'
            else:
                self.item['price_on_req'] = 'false'

            self.item['Status'] = data['projectStatus']
            if self.item['Status'] == '':
                self.item['Status'] = 'None'

            try:
                dat = int(data['verificationDate'])/1000
                self.item['listing_date'] = time.strftime('%m/%d/%Y %H:%M:%S',time.gmtime(dat))
                self.item['updated_date'] = self.item['listing_date']
            except:
                self.item['listing_date'] = dt.now().strftime('%m/%d/%Y %H:%M:%S')
                self.item['updated_date'] = self.item['listing_date']

            if 'ale' in self.item['txn_type']:
                prc_pr_sf = i.xpath('div[@class="cardWrapper"]/div[@class="cardLayout clearfix"]/div[@class="infoWrap"]/div[@class="headInfo"]/div[@class="priceWrap"]/div[@class="price-rate-col"]/div[@class="rate"]/span[@class="val"]/text()').extract_first()
                self.item['price_per_sqft'] = re.findall('[0-9]+',prc_pr_sf)
                self.item['price_per_sqft'] = ''.join(self.item['price_per_sqft'])
            else:
                self.item['price_per_sqft'] = '0'

            sqf = i.xpath('.//span[@class="size"]/text()').extract_first()
            try:
                self.item['Bua_sqft'] = re.findall('[0-9]+', sqf)
                self.item['Bua_sqft'] = ''.join(self.item['Bua_sqft'])
            except:
                self.item['Bua_sqft'] = '0'

            if 'onstruction' in self.item['Status']:
                try:
                    date = i.xpath('div[@class="cardWrapper"]/div[@class="cardLayout clearfix"]/div[@class="infoWrap"]/div[@class="highlight-points"]/div[@class="dcol poss"]/div[1]/text()').extract_first()
                    self.item['Possession'] = dt.strftime(dt.strptime(date,'%b %Y'),'%m/%d/%Y %H:%M:%S')
                except:
                    pass
                    # print date
            elif 'esale' in self.item['txn_type']:
                self.item['age'] = i.xpath('div[@class="cardWrapper"]/div[@class="cardLayout clearfix"]/div[@class="infoWrap"]/div[@class="highlight-points"]/div[@class="dcol poss"]/div[@class="val ''"]/text()').extract_first()

            self.item['scraped_time'] = dt.now().strftime('%m/%d/%Y %H:%M:%S')

            if (((not self.item['Monthly_Rent'] == '0') and (not self.item['Bua_sqft']=='0') and (not self.item['Building_name']=='None') and (not self.item['lat']=='0')) or ((not self.item['Selling_price'] == '0') and (not self.item['Bua_sqft']=='0') and (not self.item['Building_name']=='None') and (not self.item['lat']=='0')) or ((not self.item['price_per_sqft'] == '0') and (not self.item['Bua_sqft']=='0') and (not self.item['Building_name']=='None') and (not self.item['lat']=='0'))):
                self.item['quality4'] = 1
            elif (((not self.item['price_per_sqft'] == '0') and (not self.item['Building_name']=='None') and (not self.item['lat']=='0')) or ((not self.item['Selling_price'] == '0') and (not self.item['Bua_sqft']=='0') and (not self.item['lat']=='0')) or ((not self.item['Monthly_Rent'] == '0') and (not self.item['Bua_sqft']=='0') and (not self.item['lat']=='0')) or ((not self.item['Selling_price'] == '0') and (not self.item['Bua_sqft']=='0') and (not self.item['Building_name']=='None')) or ((not self.item['Monthly_Rent'] == '0') and (not self.item['Bua_sqft']=='0') and (not self.item['Building_name']=='None'))):
                self.item['quality4'] = 0.5
            else:
                self.item['quality4'] = 0
            if ((not self.item['Building_name'] == 'None') and (not self.item['listing_date'] == '0') and (not self.item['txn_type'] == 'None') and (not self.item['property_type'] == 'None') and ((not self.item['Selling_price'] == '0') or (not self.item['Monthly_Rent'] == '0'))):
                self.item['quality1'] = 1
            else:
                self.item['quality1'] = 0

            if ((not self.item['Launch_date'] == '0') or (not self.item['Possession'] == '0')):
                self.item['quality2'] = 1
            else:
                self.item['quality2'] = 0

            if ((not self.item['mobile_lister'] == 'None') or (not self.item['listing_by'] == 'None') or (not self.item['name_lister'] == 'None')):
                self.item['quality3'] = 1
            else:
                self.item['quality3'] = 0

            yield self.item

        if 'cardholder' in str(response.body):
            cur_page = int(response.url.split('=')[-1])
            next_url = '='.join(response.url.split('=')[:-1])+'='+str(cur_page+1)
            yield Request(next_url,callback=self.parse)
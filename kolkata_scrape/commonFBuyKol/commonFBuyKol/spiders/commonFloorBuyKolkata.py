import scrapy
import logging
from commonFBuyKol.items import CommonfbuykolItem
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

class CommonfloorbuykolkataSpider(scrapy.Spider):
    name = "commonFloorBuyKolkata"
    allowed_domains = ["https://www.commonfloor.com/"]
    start_urls = ['https://www.commonfloor.com/listing-search?city=Kolkata&prop_name[]=&property_location_filter[]=&use_pp=0&set_pp=1&polygon=1&page_size=30&search_intent=sale&min_inr=&max_inr=&page=1']

    custom_settings = {
            'DEPTH_LIMIT' : 10000,
            'DOWNLOAD_DELAY': 5
        }

    item = CommonfbuykolItem()

    def parse(self,response):
        hxs = Selector(response)
        data = hxs.xpath('//div[@class="row listing"]')

        for i in data:
            '''
            Extracting the urls for each property and jump to new page of that property
            '''
            url = 'https://www.commonfloor.com'+i.xpath('div[2]/div[1]/div/div/h4/a/@href').extract_first()

            yield Request(url,callback=self.parse1,dont_filter=True)
        curPage = int(response.url.split('=')[-1])
        maxPage = int(response.xpath('//div[@class="paginationTabs"]/ul/li[last()-1]/a/text()').extract_first())

        if curPage < maxPage:
            nexturl = 'https://www.commonfloor.com/listing-search?city=Kolkata&prop_name[]=&property_location_filter[]=&use_pp=0&set_pp=1&polygon=1&page_size=30&search_intent=sale&min_inr=&max_inr=&page={}'.format(str(curPage+1))
            yield Request(nexturl,callback=self.parse)

    def parse1(self,response):
        hxs = Selector(response)

        if 'listing' in str(response.url):
            '''
            Assigning default values to items 
            '''
            self.item['management_by_landlord'] = 'None'
            self.item['areacode'] = 'None'
            self.item['mobile_lister'] = 'None'
            self.item['google_place_id'] = 'None'
            self.item['Launch_date'] = '0'
            self.item['age'] = '0'
            self.item['address'] = 'None'
            self.item['sublocality'] = 'None'
            self.item['lat'] = '0'
            self.item['longt'] = '0'
            self.item['price_per_sqft'] = '0'
            self.item['listing_by'] = 'None'
            self.item['name_lister'] = 'None'
            self.item['scraped_time'] = dt.now().strftime('%m/%d/%Y %H:%M:%S')
            self.item['listing_date'] = dt.now().strftime('%m/%d/%Y %H:%M:%S')
            self.item['updated_date'] = self.item['listing_date']

            self.item['platform'] = 'commonfloor'

            self.item['city'] = 'Kolkata'

            self.item['data_id'] = response.url.split('/')[-1]

            self.item['locality'] = response.xpath('//p[@class="proj-value location-name"]/text()').extract_first()

            self.item['property_type'] = 'Residential'

            try:
                self.item['Building_name'] = response.xpath('//span[@class="subH1"]/text()').extract_first().split('in ')[-1].split(self.item['locality'])[0].replace('at ','')
            except:
                self.item['Building_name'] = 'None'

            price = response.xpath('//div[@class="project-detail row card"]/div/div[@class="row"]/div[1]/div[1]/p[@class="proj-value"]/span/text()').extract_first()
            if 'Lakh' in price:
                price = str(float(price.split(' Lakh')[0])*100000)
                self.item['Selling_price'] = price
                self.item['Monthly_Rent'] = '0'
            elif 'Crore' in price:
                price = str(float(price.split(' Crore')[0])*10000000)
                self.item['Selling_price'] = price
                self.item['Monthly_Rent'] = '0'
            else:
                self.item['Selling_price'] = '0'
                self.item['Monthly_Rent'] = '0'

            if ((self.item['Selling_price']=='0') and (self.item['Monthly_Rent']=='0')):
                self.item['price_on_req'] = 'TRUE'
            else:
                self.item['price_on_req'] = 'FALSE'

            car_area = response.xpath('//div[@class="project-detail row card"]/div/div[@class="row"]/div[1]/div[2]/p[@class="proj-value"]/text()').extract_first()
            if (not '-' in car_area):
                self.item['carpet_area'] = car_area.split(' ')[0]
            else:
                self.item['carpet_area'] = '0'

            self.item['config_type'] = response.xpath('//div[@class="project-unit row card unit-detail-widget"]/div/div[@class="row"]/div/div[@class="row firstRow"]/div[1]/p/span[1]/text()').extract_first()+'BHK'
            self.item['config_type'] = self.item['config_type'].replace(' ','')

            self.item['txn_type'] = response.xpath('//div[@class="project-unit row card unit-detail-widget"]/div/div[@class="row"]/div/div[@class="row otherDetails"]/div[1]/p[2]/text()').extract_first()

            try:
                if 'New' in self.item['txn_type']:
                    self.item['txn_type'] = 'Sale'
                    dates = response.xpath('//div[@class="project-detail row card"]/div/div[@class="row"]/div[2]/div[1]/p[2]/text()').extract_first().replace("'",'20')
                    self.item['Possession'] = dt.strftime(dt.strptime(dates,"%b%Y"),"%m/%d/%Y %H:%M:%S")
                else:
                    self.item['Possession'] = '0'
            except:
                logging.log(logging.ERROR,dates)
                self.item['Possession'] = '0'

            self.item['Details'] = response.xpath('//p[@class="propStatus"]/text()').extract()

            titl = response.xpath('//div[@class="row otherDetails"]/*/p[@class="title"]/text()').extract()
            no = titl.index('Listed on')
            
            try:
                list1 = self.item['Details'][no]
                self.item['listing_date'] = dt.strftime(dt.strptime(list1,"%d %b"),"%m/%d")+"/2016 00:00:00"
                self.item['updated_date'] = self.item['listing_date']
            except:
                try:
                    list1 = self.item['Details'][no-1]
                    self.item['listing_date'] = dt.strftime(dt.strptime(list1,"%d %b"),"%m/%d")+"/2016 00:00:00"
                    self.item['updated_date'] = self.item['listing_date']
                except:
                    self.item['listing_date'] = dt.now().strftime('%m/%d/%Y %H:%M:%S')
                    self.item['updated_date'] = self.item['listing_date']

            self.item['Bua_sqft'] = [ area for area in self.item['Details'] if 'Sq. Ft.' in area][0].replace(' Sq. Ft.','')

            self.item['Status'] = response.xpath('//*[@id="page_container"]/div[2]/div/div/div[1]/div[1]/div[1]/div[2]/div/div/div/div[2]/div[1]/p[2]/@title').extract_first()

            #self.item['Status'] = [stat for stat in self.item['Details'] if (('Unfurnished' in stat) or ('semi' in stat) or ('fully' in stat))]
            #self.item['Status'] = ''.join(self.item['Status'])

            self.item['Details'] = ' '.join(self.item['Details'])

            try:
                listin = response.xpath('//*[@id="page_container"]/div[2]/div/div/div[1]/div[1]/div[1]/div[2]/div/div/div/div[2]/div[4]/p[2]/@title').extract_first()
                if 'Owner' in listin:
                    self.item['listing_by'] = 'Owner'
                elif 'Builder' in listin:
                    self.item['listing_by'] = 'Builder'
                elif 'Broker' in listin:
                    self.item['listing_by'] = 'Agent'
                elif 'Agent' in listin:
                    self.item['listing_by'] = 'Agent'
                else:
                    self.item['listing_by'] = 'None'

                self.item['name_lister'] = listin.split('(')[0]
            except:
                self.item['listing_by'] = 'None'
                self.item['name_lister'] = 'None'

            #self.item['scraped_time'] = dt.now().strftime('%m/%d/%Y %H:%M:%S')

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

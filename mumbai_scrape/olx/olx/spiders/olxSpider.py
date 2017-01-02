from scrapy.selector import Selector
from olx.items import OlxItem
from scrapy.spiders import CrawlSpider, Rule
from scrapy.http import Request
import re
from datetime import datetime as dt
from datetime import time,timedelta
from datetime import date as d
import time

class MySpider(CrawlSpider):
    name = "olxMumbai"
    allowed_domains = ['www.olx.in']
    start_urls = ['https://www.olx.in/mumbai/real-estate/']

    item = OlxItem()
 
    def parse(self, response):
        hxs = Selector(response)
        data = hxs.xpath('//*[@id="offers_table"]/tbody/tr/td[contains(@class,"offer")]')

        for i in data:
            typ = i.xpath('table/tbody/tr/td[@valign="top"]/p/small/text()').extract_first().strip()
            if (('Apartments' in typ) or ('Shops' in typ) or ('Houses' in typ)):
                url = i.xpath('table/tbody/tr/td[@valign="top"]/h3/a/@href').extract_first()
                
                yield Request(url,callback=self.parse1,dont_filter=True)

        if 'Next page' in response.xpath('//div[@class="pager rel clr"]/span[last()]/a/span/text()').extract_first():
            next_url = response.xpath('//div[@class="pager rel clr"]/span[last()]/a/@href').extract_first()
            
            yield Request(next_url,callback=self.parse)

    def parse1(self,response):
        hxs = Selector(response)

        '''
        Assigning default value
        '''
        self.item['Selling_price'] = '0'
        self.item['Monthly_Rent'] = '0'
        self.item['lat'] = '0'
        self.item['longt'] = '0'
        self.item['Bua_sqft'] = '0'
        self.item['carpet_area'] = '0'
        self.item['price_per_sqft'] = '0'
        self.item['management_by_landlord'] = 'None'
        self.item['areacode'] = 'None'
        self.item['mobile_lister'] = 'None'
        self.item['google_place_id'] = 'None'
        self.item['Launch_date'] = 'None'
        self.item['Possession'] = '0'
        self.item['age'] = 'None'
        self.item['address'] = 'None'
        self.item['price_on_req'] = 'false'
        self.item['sublocality'] = 'None'
        self.item['config_type'] = 'None'
        self.item['listing_date'] = dt.now().strftime('%m/%d/%Y %H:%M:%S')
        self.item['updated_date'] = self.item['listing_date']
        self.item['txn_type'] = 'None'
        self.item['property_type'] = 'None'
        self.item['Building_name'] = 'None'
        self.item['locality'] = 'None'
        self.item['price_per_sqft'] = '0'
        self.item['Bua_sqft'] = '0'
        self.item['Status'] = 'None'
        self.item['listing_by'] = 'None'
        self.item['name_lister'] = 'None'
        self.item['Details'] = 'None'

        self.item['city'] = 'mumbai'
        self.item['platform'] = 'olx'

        self.item['data_id'] = response.xpath('//span[@class="rel inlblk"]/text()').extract_first().strip()

        lat_long = response.xpath('//div[@id="mapcontainer"]/@class').extract_first()
        
        self.item['lat'] = re.findall(" lat: '([0-9.]+)'",lat_long)[0]

        self.item['longt'] = re.findall(" lon: '([0-9.]+)'",lat_long)[0]

        self.item['locality'] = response.xpath('//strong[@class="c2b small"]/text()').extract_first().strip()

        typ = response.xpath('//*[@id="breadcrumbTop"]/tr/td/ul/li[3]/a/span/text()').extract_first().strip()
        if 'ale' in typ:
            self.item['txn_type'] = 'Sale'
        if 'ent' in typ:
            self.item['txn_type'] = 'Rent'

        if 'ale' in self.item['txn_type']:
            self.item['Selling_price'] = response.xpath('//strong[@class="xxxx-large margintop7 inlblk not-arranged"]/text()').extract_first()
            self.item['Monthly_Rent'] = '0'
        if 'ent' in self.item['txn_type']:
            self.item['Monthly_Rent'] = response.xpath('//strong[@class="xxxx-large margintop7 inlblk not-arranged"]/text()').extract_first()
            self.item['Selling_price'] = '0'

        prp_typ = response.xpath('//*[@id="breadcrumbTop"]/tr/td/ul/li[4]/a/span/text()').extract_first().strip()
        if (('Apartments' in prp_typ) or ('Houses' in prp_typ)):
            self.item['property_type'] = 'Residential'
        if ('Shops' in prp_typ):
            self.item['property_type'] = 'Commercial'

        try:
            conf = response.xpath('//a[contains(@title,"room")]/text()').extract_first().strip()
            if (not conf==None):
                self.item['config_type'] = re.findall('[0-9]',conf)[0]+'BHK'
        except:
            try:
                conf1 = response.xpath('//a[contains(@title,"more")]/text()').extract_first().strip()
                if (not conf1==None):
                    self.item['config_type'] = re.findall('[0-9]',conf1)[0]+'BHK'
            except:
                print 'No config '+' -->>'+str(response.url)
                self.item['config_type'] = 'None'

        dates = response.xpath('//span[@class="pdingleft10 brlefte5"]/text()').extract()
        date1 = ' '.join(re.findall('[\S]+',[date for date in dates if re.findall('[\w]',date)][0])).replace(',','').replace('on ','').replace('at ','').replace('Added ','')
        if 'terday' in date1:
            self.item['listing_date'] = str((d.today() - timedelta(days=1)).month)+"/"+str((d.today() - timedelta(days=1)).day)+"/"+str((d.today() - timedelta(days=1)).year) + ' 00:00:00'
        elif 'oday' in date1:
            self.item['listing_date'] = str(d.today().month)+'/'+str(d.today().day)+'/'+str(d.today().year) + ' 00:00:00'
        elif ((' am' in date1) or (' pm' in date1)):
            self.item['listing_date'] = str(d.today().month)+'/'+str(d.today().day)+'/'+str(d.today().year) +' '+ date1.replace(' am','').replace(' pm','') + ':00'
        else:
            self.item['listing_date'] = dt.strftime(dt.strptime(date1,'%d %b'),'%m/%d')+'/'+str(d.today().year) + ' 00:00:00'

        self.item['updated_date'] = self.item['listing_date']

        try:
            area = response.xpath('//strong[@class="block"]/text()').extract()
            get_area = [sqf for sqf in area if ' ft' in sqf]
            if get_area:
                self.item['Bua_sqft'] = re.findall('[0-9,]+',get_area[0].strip())[0]
                if ',' in self.item['Bua_sqft']:
                    self.item['Bua_sqft'] = self.item['Bua_sqft'].replace(',','')
        except:
            print 'No Sqft -->>'+str(response.url)

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
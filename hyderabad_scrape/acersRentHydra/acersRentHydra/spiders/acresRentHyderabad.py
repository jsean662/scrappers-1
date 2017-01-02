import scrapy
from acersRentHydra.items import AcersrenthydraItem
from scrapy.spiders import Spider
from scrapy.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.http import Request
from scrapy.selector import Selector
from scrapy.selector import HtmlXPathSelector
from urlparse import urljoin
import time
import datetime
from datetime import datetime as dt
import re


class AcresrenthyderabadSpider(scrapy.Spider):
    name = "acresRentHyderabad"
    allowed_domains = ["http://www.99acres.com/"]
    start_urls = ['http://www.99acres.com/rent-property-in-hyderabad-ffid-page-%s?orig_property_type=1,4,2,90&search_type=QS&search_location=CP12&lstacn=SEARCH&pageid=QS&src=PAGING&property_type=1,4,2,90/'% page for page in xrange(1,101)]
    custom_settings = {
            'DEPTH_LIMIT': 3000,
            'DOWNLOAD_DELAY': 12
        }
    def parse(self, response):
        
        hxs = Selector(response)
        path1 = "//div[@id='ysf']/h1"
        x1 = hxs.xpath(path1)
        path = "//div[@id='results']/div[1]/div[contains(@class,'srpWrap')]"
        x = hxs.xpath(path)
        for i in x:
            item = AcersrenthydraItem()

            
            data_id = i.xpath("@data-propid").extract_first()
            
            try:
                sqft_check = i.xpath(".//div[@class='srpDataWrap']/span[1]/b[1]/text()").extract_first().replace(' ', '')
                print("sqft_check: ", sqft_check)

                if 'Sq.Ft.' in sqft_check:
                    sqft_check = re.findall('[0-9]+',sqft_check)
                elif 'Sq. Yards' in sqft_check:
                    sqft_check = re.findall('[0-9]+',sqft_check)
                    sqft_check = [str(int(x)*9) for x in sqft_check]
                elif 'Sq. Meter' in sqft_check:
                    sqft_check = re.findall('[0-9]+',sqft_check)
                    sqft_check = [str(int(float(x)*10.7639)) for x in sqft_check]
                elif 'Guntha' in sqft_check:
                    sqft_check = sqft_check.replace('Guntha', '')
                    sqft_check = [str(eval(sqft_check)*1089)]
                elif 'Kottah' in sqft_check:
                    sqft_check = sqft_check.replace('Kottah', '')
                    sqft_check = [str(eval(sqft_check)*720)]
                    print("Kottah: ", sqft_check)
                else:
                    sqft_check = re.findall('[0-9]+',sqft_check)
            except:
                sqft_check = '0'

            #print("sqft_check: ", sqft_check)
            
            item['Possession'] = '0'
            item['Monthly_Rent'] = '0'
            item['config_type'] = 'None'
            item['age'] = '0'
            item['lat'] = '0'
            item['longt'] = '0'
            item['address'] = 'None'
            item['locality'] = 'None'
            item['sublocality'] = 'None'
            item['google_place_id'] = 'None'
            item['Launch_date'] = '0'
            item['mobile_lister'] = 'None'
            item['areacode'] = 'None'
            item['management_by_landlord'] = 'None'
            item['carpet_area'] = '0'
            item['details'] = 'None'
            item['property_type'] = 'None'
            item['Selling_price'] = '0'
            item['scraped_time'] = dt.now().strftime('%m/%d/%Y %H:%M:%S')

        
            item['city'] = "Kolkata"
            sqft_check = str(sqft_check).replace(',', '.').replace('[', '').replace(']', '').replace("'", "").replace('u', '').replace(' ', '')
            item['Bua_sqft'] =  sqft_check
            
            try:
                item['price_per_sqft'] = i.xpath(".//div[@class='srpDataWrap']/span/text()").extract()
                item['price_per_sqft'] = ''.join(item['price_per_sqft'])
                if 'Sq.Ft.' in item['price_per_sqft']:
                    item['price_per_sqft'] = re.findall('[0-9]+',item['price_per_sqft'])
                    if item['price_per_sqft']:
                        item['price_per_sqft'] = item['price_per_sqft'][0]
                elif 'Sq. Yards' in item['price_per_sqft']:
                    item['price_per_sqft'] = re.findall('[0-9]+',item['price_per_sqft'])
                    if item['price_per_sqft']:
                        item['price_per_sqft'] = str(int(item['price_per_sqft'][0])/9)
                elif 'Sq. Meter' in item['price_per_sqft']:
                    item['price_per_sqft'] = re.findall('[0-9]+',item['price_per_sqft'])
                    if item['price_per_sqft']:
                        item['price_per_sqft'] = str(int(float(item['price_per_sqft'][0])/10.7639))
                else:
                    item['price_per_sqft'] = re.findall('[0-9]+',item['price_per_sqft'])
                    if item['price_per_sqft']:
                        item['price_per_sqft'] = item['price_per_sqft'][0]
                if not item['price_per_sqft']:
                    item['price_per_sqft'] = '0'
            except:
                item['price_per_sqft'] = '0' 

           
            price = i.xpath('.//b[@itemprop="price"]/text()').extract_first()
            if price:
                if 'Lac' in price:
                    price = str(float(str(price.split()[0])) * 100000)
                    item['Monthly_Rent'] = price
                elif 'Crore' in price:
                    price =  str(float(str(price.split()[0])) * 10000000)
                    item['Monthly_Rent'] = price
                else:
                    item['Monthly_Rent'] = price.replace(',','')
                    item['Selling_price'] = '0'
            else:
                item['Selling_price'] = '0'
                item['Monthly_Rent'] = '0'
            if 'Request' in item['Monthly_Rent']:
                item['Selling_price'] = '0'
                item['Monthly_Rent'] = '0'
            
            
            if item['Monthly_Rent'] == '0' and item['Selling_price'] == '0':
                item['price_on_req'] = 'TRUE'
            else:
                item['price_on_req'] = 'FALSE' 
            
            #item['Bua_sqft'] = sqft_check
            #print(sqft_check)
            
            item['platform'] = '99acres'
            item['Status'] = 'Ready to move'
            item['txn_type'] = "Rent"
            item['data_id'] = data_id

            item['Building_name'] = str(i.xpath("div[@class='srpDetail']/div[@class='srpDataWrap']/span[2]/a/b/text()").extract_first(default="None"))
            if not item['Building_name'] == '':
                item['Building_name'] = item['Building_name'].replace("\n", "").strip()


            status = str(i.xpath("div[@class='srpDetail']/div[@class='srpDataWrap']/span[3]/span[2]/text()").extract()).replace('\\xa0','').replace(',','').replace("'","").strip()
            if 'Rent' in status:

                ###########  FOR age MAX value is taken  ###########

                item['age'] = str(i.xpath("div[@class='srpDetail']/div[@class='srpDataWrap']/span[3]/span[3]/text()").extract()).replace('\\xa0','').replace(',','').replace("'","").replace("[","").replace("]","").replace(" years old", "").replace("+", "").strip().split()[-1]
                if 'Furnished' in item['age'] or 'Immediate' in item['age'] or 'Unfurnished' in item['age'] or 'Semifurnished' in item['age']:
                    item['age'] = '0'
                    item['Possession'] = '0'
                item['Possession'] = '0'
            else:
                item['age'] = '0'
                item['Possession'] = '0'

            try:
                date_string = str(i.xpath("div[@class='srpDetail']/div[last()]/text()").extract()).split(':')[-1].replace(' ','').replace(']','').replace('\\n','').replace("'","").replace('[', '').replace(']', '').replace('u', '').strip()
                if date_string == 'Today':
                    date = time.strftime('%b%d,%Y')
                else:
                    if date_string == 'Yesterday':
                        date = dt.strftime(dt.now()-datetime.timedelta(1),'%b%d,%Y')
                    else:
                        date = date_string
                date = dt.strftime(dt.strptime(date,'%b%d,%Y'),'%m/%d/%Y %H:%M:%S')
                item['listing_date'] = date
            except:
                item['listing_date'] = time.strftime('%b%d,%Y')

            try:
                item['lat'] = i.xpath("div[@class='wrapttl']/i/@data-maplatlngzm").extract_first().split(",")[0]
            except:
                item['lat'] = '0'
            try:
                item['longt'] = i.xpath("div[@class='wrapttl']/i/@data-maplatlngzm").extract_first().split(",")[1]
            except:
                item['longt'] = '0'
            
            try:
                item['property_type'] = i.xpath('.//meta[@itemprop="name"]/@content').extract_first().replace("for rent")
                if 'Studio' in item['property_type']:
                    item['property_type'] = "Studio Apartment"
            except:
                item['property_type'] = 'Residential'

            try:
                
                item['locality'] = i.xpath("div[@class='wrapttl']/div[1]/a/text()").extract_first().split('in')[-1].strip()
            except:
                item['locality'] = i.xpath('.//meta[@itemprop="addressLocality"]/@content').extract_first(default='None')

            try:
                item['Building_name'] = i.xpath(".//div[@class='srpDataWrap']/span[2]/a[@class='sName']/b/text()").extract_first().strip()
            except:
                item['Building_name'] = 'None'

            if 'Studio Apartment' in item['property_type']:
                item['config_type'] = '1RK'
            else:
                con1 = i.xpath("div[@class='wrapttl']/div[1]/a/text()").extract_first()
                conf = str(re.findall('[0-9]+',con1)[0])
                item['config_type'] = conf+'BHK'

            if item['config_type'] == 'BHK':
                item['config_type'] = 'None'

            
            try:
                build = i.xpath("div[@class='srpDetail']/div[last()]/text()").extract()[0].encode('ascii', 'ignore').decode('ascii')
                if 'Builder' in build:
                    item['listing_by'] = 'Builder'
                    item['name_lister'] = build.split(' Posted')[0].split(':')[-1].strip()
                elif 'Owner' in build:
                    item['listing_by'] = 'Owner'
                    item['name_lister'] = build.split(' Posted')[0].split(':')[-1].strip()
                else:
                    item['listing_by'] = 'None'
                    item['name_lister'] = 'None'
            except:
                item['listing_by'] = 'None'
                item['name_lister'] = 'None'

            try:
                date_string = i.xpath('.//div[@class="lf f13 hm10 mb5"]/text()').extract_first().split(':')[-1].strip().replace(' ','').replace(',','')
                #print(date_string)
                if date_string=='':
                    date_string = i.xpath('.//div[@class="lf f13 hm10 mb5"]/text()').extract()[-1].strip().split(':')[-1].replace(' ','').replace(',','')
                if 'Today' in date_string:
                    date = time.strftime('%b%d%Y')
                elif 'Yesterday' in date_string:
                    date = dt.strftime(dt.now()-datetime.timedelta(1),'%b%d%Y')
                else:
                    date = date_string
                item['listing_date'] = dt.strftime(dt.strptime(date,'%b%d%Y'),'%m/%d/%Y %H:%M:%S')
                item['updated_date'] = item['listing_date']
            except:
                item['listing_date'] = '0'
                item['updated_date'] = item['listing_date']

            if (((not item['Monthly_Rent'] == '0') and (not item['Bua_sqft']=='0') and (not item['Building_name']=='None') and (not item['lat']=='0')) or ((not item['Selling_price'] == '0') and (not item['Bua_sqft']=='0') and (not item['Building_name']=='None') and (not item['lat']=='0')) or ((not item['price_per_sqft'] == '0') and (not item['Bua_sqft']=='0') and (not item['Building_name']=='None') and (not item['lat']=='0'))):
                item['quality4'] = 1
            elif (((not item['price_per_sqft'] == '0') and (not item['Building_name']=='None') and (not item['lat']=='0')) or ((not item['Selling_price'] == '0') and (not item['Bua_sqft']=='0') and (not item['lat']=='0')) or ((not item['Monthly_Rent'] == '0') and (not item['Bua_sqft']=='0') and (not item['lat']=='0')) or ((not item['Selling_price'] == '0') and (not item['Bua_sqft']=='0') and (not item['Building_name']=='None')) or ((not item['Monthly_Rent'] == '0') and (not item['Bua_sqft']=='0') and (not item['Building_name']=='None'))):
                item['quality4'] = 0.5
            else:
                item['quality4'] = 0

            if ((not item['mobile_lister'] == 'None') or (not item['listing_by'] == 'None') or (not item['name_lister'] == 'None')):
                item['quality3'] = 1
            else:
                item['quality3'] = 0              

            if ((not item['Launch_date'] == '0') or (not item['Possession'] == '0')):
                item['quality2'] = 1
            else:
                item['quality2'] = 0

            if ((not item['Building_name'] == 'None') and (not item['listing_date'] == '0') and (not item['txn_type'] == 'None') and (not item['property_type'] == 'None') and ((not item['Selling_price'] == '0') or (not item['Monthly_Rent'] == '0'))):
                item['quality1'] = 1
            else:
                item['quality1'] = 0

            
            yield item

import scrapy
from acers.items import AcersItem
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


class AcersspiderSpider(scrapy.Spider):
    name = "acersBuyPune"
    allowed_domains = ["http://www.99acres.com/"]
    start_urls = ['http://www.99acres.com/property-in-pune-ffid-page-%s?orig_property_type=1,4,2,90&search_type=QS&search_location=CP12&pageid=QS&keyword_orig=pune&property_type=1,4,2,90' % page for page in xrange(1,955)]
    custom_settings = {
            'DEPTH_LIMIT': 3000,
            'DOWNLOAD_DELAY': 15
        }

    def parse(self, response):
        hxs = Selector(response)
        path1 = "//div[@id='ysf']/h1"
        x1 = hxs.xpath(path1)
        path = "//div[@id='results']/div[1]/div[contains(@class,'srpWrap')]"
        x = hxs.xpath(path)
        for i in x:
            item = AcersItem()

            
            data_id = i.xpath("@data-propid").extract_first()
            
            sqft_check = i.xpath("div[@class='srpDetail']/div[@class='srpDataWrap']/span[1]/b[1]/text()").extract_first()
            #print("sqft_check: ", sqft_check)

            if 'Sq.Ft.' in sqft_check:
                sqft_check = re.findall('[0-9]+',sqft_check)
            elif 'Sq. Yards' in sqft_check:
                sqft_check = re.findall('[0-9]+',sqft_check)
                sqft_check = [str(int(x)*9) for x in sqft_check]
            elif 'Sq. Meter' in sqft_check:
                sqft_check = re.findall('[0-9]+',sqft_check)
                sqft_check = [str(int(float(x)*10.7639)) for x in sqft_check]
            else:
                sqft_check = re.findall('[0-9]+',sqft_check)

            #print("sqft_check: ", sqft_check)
            check = 0
            
            for s in sqft_check:
                check = check + 1    
                
                item['Possession'] = '0'
                item['Monthly_Rent'] = '0'
                item['txn_type'] = 'None'
                item['Status'] = 'None'
                item['config_type'] = 'None'
                item['age'] = '0'
                item['lat'] = '0'
                item['longt'] = '0'
                item['address'] = 'None'
                item['sublocality'] = 'None'
                item['google_place_id'] = 'None'
                item['Launch_date'] = '0'
                item['mobile_lister'] = 'None'
                item['areacode'] = 'None'
                item['management_by_landlord'] = 'None'
                item['carpet_area'] = '0'
                item['Details'] = 'None'  

            
                item['city'] = "Pune"
                item['scraped_time'] = dt.now().strftime('%m/%d/%Y %H:%M:%S')
                item['Bua_sqft'] =  s
                
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
                    if 'to' in price:
                        price1 = price.split('to')[0]
                        price2 = price.split('to')[1]
                    
                        if 'Lac' in price1:
                            price1 = float(str(price1.split()[0])) * 100000
                        else:
                            if 'Crore' in price1:
                                price1 =  float(str(price1.split()[0])) * 10000000
                        if 'Lac' in price2:
                            price2 = float(str(price2.split()[0])) * 100000
                        else:
                            if 'Crore' in price2:
                                price2 =  float(str(price2.split()[0])) * 10000000
                        if check == 1:
                            price = str(price1)
                        else:
                            price = str(price2)
                    else:
                        if 'Lac' in price:
                            price = str(float(str(price.split()[0])) * 100000)
                        else:
                            if 'Crore' in price:
                                price =  str(float(str(price.split()[0])) * 10000000)
                    item['Selling_price'] = price
                    item['Monthly_Rent'] = '0'
                else:
                    item['Selling_price'] = '0'
                    item['Monthly_Rent'] = '0'
                if 'Request' in item['Selling_price']:
                    item['Selling_price'] = '0'
                    item['Monthly_Rent'] = '0'
                
                
                if item['Monthly_Rent'] == '0' and item['Selling_price'] == '0':
                    item['price_on_req'] = 'TRUE'
                else:
                    item['price_on_req'] = 'FALSE' 


                
                #item['Bua_sqft'] = sqft_check
                #print(sqft_check)
                item['data_id'] = data_id
                item['platform'] = '99acres'

                item['txn_type'] = x1.xpath("span[2]/b/text()").extract_first()

                item['city'] = x1.xpath("span[3]/b/text()").extract_first().split(" ")[0]

                item['Building_name'] = str(i.xpath("div[@class='srpDetail']/div[@class='srpDataWrap']/span[2]/a/b/text()").extract_first(default="None"))
                if not item['Building_name'] == '':
                    item['Building_name'] = item['Building_name'].replace("\n", "").strip()

                item['Status'] = str(i.xpath("div[@class='srpDetail']/div[@class='srpDataWrap']/span[3]/span[2]/text()").extract()).replace('\\xa0','').replace('u','').replace(',','').replace("'","").replace("[","").replace("]","")
                if (item['Status'] == "Resale") or (item['Status'] == "New Booking"):
                    item['Status'] = "Resale"

                item['Status'] = str(i.xpath("div[@class='srpDetail']/div[@class='srpDataWrap']/span[3]/span[3]/text()").extract()).replace('\\xa0','').replace('u','').replace(',','').replace("'","").replace("[","").replace("]","").strip()
                if item['Status'] == "Under Constrction":
                    try:
                        dat = str(i.xpath("div[@class='srpDetail']/div[@class='srpDataWrap']/span[3]/span[4]/text()").extract()).replace('\\xa0','').replace(',','').replace("'","").replace("[","").replace("]","").replace("Possession By ", "").strip().split()[-2:]
                        dat = ' '.join(dat)
                        #print(dat)
                        item['Possession'] = dt.strftime(dt.strptime(dat, '%b %Y'),'%m/%d/%Y %H:%M:%S')
                        item['age'] = 0
                    except:
                        item['Possession'] = 0
                        item['age'] = 0
                        
                elif item['Status'] == "Ready to move":
                    
                    #############  FOR age MAX age is taken   #####################

                    item['age'] = str(i.xpath("div[@class='srpDetail']/div[@class='srpDataWrap']/span[3]/span[4]/text()").extract()).replace('\\xa0','').replace(',','').replace("'","").replace("[","").replace("]","").replace(" years old", "").replace("+", "").replace("u", "").strip().split()[-1]
                    item['Possession'] = 0

                date_string = str(i.xpath("div[@class='srpDetail']/div[last()]/text()").extract()).split(':')[-1].replace(' ','').replace(']','').replace('\\n','').replace("'","")
                if date_string == 'Today':
                    date = time.strftime('%b%d,%Y')
                else:
                    if date_string == 'Yesterday':
                        date = dt.strftime(dt.now()-datetime.timedelta(1),'%b%d,%Y')
                    else:
                        date = date_string
                date = dt.strftime(dt.strptime(date,'%b%d,%Y'),'%m/%d/%Y %H:%M:%S')
                item['listing_date'] = date

                try:
                    item['lat'] = i.xpath("div[@class='wrapttl']/i/@data-maplatlngzm").extract_first().split(",")[0]
                except:
                    item['lat'] = '0'
                    
                try:
                    item['longt'] = i.xpath("div[@class='wrapttl']/i/@data-maplatlngzm").extract_first().split(",")[1]
                except:
                    item['longt'] = '0'
                
                try:
                    item['property_type'] = i.xpath('.//meta[@itemprop="name"]/@content').extract_first()
                    if 'Studio' in item['property_type']:
                        item['property_type'] = "Studio Apartment"
                except:
                    item['property_type'] = 'Residential Apartment'

                try:
                    item['locality'] = i.xpath('.//meta[@itemprop="addressLocality"]/@content').extract_first()
                except:
                    item['locality'] = 'None'

                try:
                    item['Building_name'] = i.xpath(".//div[@class='srpDataWrap']/span[2]/a[@class='sName']/b/text()").extract_first().strip()
                except:
                    item['Building_name'] = 'None'

                if 'Studio Apartment' in item['property_type']:
                    item['config_type'] = '1RK'
                else:
                    con1 = i.xpath("div[@class='wrapttl']/div[1]/a/text()").extract_first()
                    conf = re.findall('[0-9]+',con1)[0]
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

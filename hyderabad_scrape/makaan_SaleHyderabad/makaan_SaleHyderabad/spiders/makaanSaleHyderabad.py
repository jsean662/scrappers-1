# -*- coding: utf-8 -*-
import scrapy
from ..items import MakaanSalehyderabadItem
from scrapy.selector import Selector
import re
from scrapy.http import Request
import json
import datetime
from datetime import datetime as dt


class MakaansalehyderabadSpider(scrapy.Spider):
    name = "Makaan_Hyderabad"
    allowed_domains = ["makaan.com"]
    start_urls = [
        'https://www.makaan.com/listings?sortBy=date-desc&listingType=buy&pageType=LISTINGS_PROPERTY_URLS&cityName=Hyderabad&cityId=12&templateId=MAKAAN_CITY_LISTING_BUY&format=json&page=1',
        'https://www.makaan.com/listings?sortBy=date-desc&listingType=rent&pageType=LISTINGS_PROPERTY_URLS&cityName=Hyderabad&cityId=12&templateId=MAKAAN_CITY_LISTING_BUY&format=json&page=1',
    ]
    custom_settings = {
        'DEPTH_LIMIT': 10000,
        'DOWNLOAD_DELAY': 5.0,
    }

    def parse(self, response):
        item = MakaanSalehyderabadItem()
        # hxs = Selector(response)
        a = response.xpath('//div[@class="cardholder"]')
        # '//*[@id="mod-listingsWrapper-1"]/div/div[1]/div[2]/div[@class="cardholder"]'

        for i in a:
            try:

                detail = i.xpath('.//div[contains(@class,"cardWrapper")]/script/text()').extract_first()
                data = json.loads(detail)
                # print('Data : ', data)

                item['carpet_area'] = '0'
                item['updated_date'] = '0'
                item['management_by_landlord'] = 'None'
                item['areacode'] = '0'
                item['mobile_lister'] = '0'
                item['google_place_id'] = 'None'
                age = item['age'] = '0'
                item['address'] = 'None'
                item['price_on_req'] = 'FALSE'
                item['sublocality'] = 'None'
                item['config_type'] = 'None'
                item['platform'] = 'None'
                item['city'] = 'None'
                item['listing_date'] = '0'
                item['txn_type'] = 'None'
                item['property_type'] = 'None'
                item['Building_name'] = 'None'
                item['lat'] = '0'
                item['longt'] = '0'
                item['locality'] = 'None'
                item['Status'] = 'None'
                item['listing_by'] = 'None'
                item['name_lister'] = 'None'
                item['Selling_price'] = '0'
                item['Monthly_Rent'] = '0'
                item['Details'] = 'None'
                item['data_id'] = 'None'
                item['Possession'] = '0'
                item['Launch_date'] = '0'
                item['price_per_sqft'] = '0'
                item['Bua_sqft'] = '0'
                item['quality1'] = '0'
                item['quality2'] = '0'
                item['quality3'] = '0'
                item['quality4'] = '0'

                item['property_type'] = data['propertyType']
                if item['property_type'] is None:
                    item['property_type'] = 'Residential'
                if item['property_type'] is not None:
                    if 'other' in item['property_type'] or 'Other' in item['property_type']:
                        item['property_type'] = 'Residential'

                item['platform'] = 'Makaan'

                item['data_id'] = data['id']

                item['name_lister'] = data['companyName']
                if item['name_lister'] == '':
                    item['name_lister'] = 'None'

                item['listing_by'] = data['companyType']

                item['mobile_lister'] = data['companyPhone']

                item['lat'] = data['latitude']
                if item['lat'] == '':
                    item['lat'] = '0'

                item['longt'] = data['longitude']
                if item['longt'] == '':
                    item['longt'] = '0'

                item['locality'] = data['localityName']

                item['city'] = data['cityName']

                buildname = data['fullName']
                if buildname == '' or buildname is None: 
                    buildname = 'None'
                
                buildname = buildname.lower().strip()

                if 'bhk' in buildname:
                    buildname = buildname.replace('bhk', '').replace(''.join(re.findall('[0-9]+', buildname)), '')

                if 'floor ' in buildname or ' floor' in buildname:
                    buildname = buildname.replace('floor', '').replace(''.join(re.findall('[0-9]+', buildname)), '').replace('th', '').replace('st', '')

                if 'other' in buildname:
                    buildname = buildname.replace('other', '').replace('others', '')
                
                if 'reputed' in buildname:
                    buildname = buildname.replace('reputed', '').replace('builder', '')
                
                re.sub('chowk', '', buildname)

                if ' road' in buildname:
                    buildname = buildname.split('road ')[1]

                if 'lane ' in buildname:
                    buildname = buildname.split('lane ')[0]

                if 'behind ' in buildname:
                    buildname = buildname.split('behind ')[0]
                
                if 'near ' in buildname:
                    buildname = buildname.split('near ')[0]
                
                if 'opposite' in buildname or ' opp ' in buildname or ' opp.' in buildname:
                    buildname = buildname.split(' opp')[0]

                if ' from ' in buildname or ' for ' in buildname:
                    buildname = 'None'

                if 'on req' in buildname:
                    buildname = 'None'

                if ' at ' in buildname:
                    buildname = buildname.split(' at ')[1]

                if ' in ' in buildname:
                    buildname = buildname.split(' in ')[1]

                if 'xyz ' in buildname or 'abc ' in buildname:
                    buildname = 'None'

                buildname = str(buildname).strip()

                if buildname.isdigit() and len(buildname) > 4:
                    buildname = 'None'

                if buildname == 'abc' or buildname == 'abcd' or buildname == 'xyz' or buildname == 'pqr':
                    buildname = 'None'

                if buildname == 'chs' or buildname == 'hs' or buildname == 'society' or buildname == 'project' or buildname == 'apartment' or buildname == 'heights':
                    buildname = 'None'

                buildname = buildname.title()
                if buildname == '' or buildname == ' ':
                    buildname = 'None'
                item['Building_name'] = buildname

                config = data['bedrooms']
                if config is None or config == '' or config == ' ':
                    config = 'None'
                else:
                    config += 'BHK'

                item['config_type'] = config

                # item['txn_type'] = data['listingCategory']

                # if 'Primary' in item['txn_type']:
                #     item['txn_type'] = 'Sale'
                if 'listingType=buy' in str(response.url):
                    item['txn_type'] = 'Sale'
                elif 'listingType=rent' in str(response.url):
                    item['txn_type'] = 'Rent'

                if item['txn_type'] == 'Sale' or item['txn_type'] == 'Resale':
                    item['Selling_price'] = data['price']
                    item['Monthly_Rent'] = '0'

                if 'Rent' in item['txn_type']:
                    item['Monthly_Rent'] = data['price']
                    item['Selling_price'] = '0'

                if item['Selling_price'] == '0' and item['Monthly_Rent'] == '0':
                    item['price_on_req'] = 'TRUE'
                else:
                    item['price_on_req'] = 'FALSE'

                if 'ale' in item['txn_type']:
                    item['Status'] = data['projectStatus']
                    if 'progress' in item['Status'] or item['Status'] == '' or item['Status'] is None:
                        item['Status'] = 'Under Construction'
                        aval = i.xpath('.//div[@class="listing-details"]/span[contains(@title,"by")]/span/strong/text()').extract_first()
                        if aval is not None:
                            aval = aval.split('by ')[1]
                            item['Possession'] = dt.strftime(dt.strptime(aval, '%b %Y'), '%m/%d/%Y')
                    else:
                        item['Possession'] = '0'
                elif 'ent' in item['txn_type']:
                    item['Status'] = i.xpath('.//*[contains(@class,"hcol w44")]/div[1]/text()').extract_first(default='None')
                    aval = i.xpath('//div[@class="listing-details"]/span[@title="availability"]/span/strong/text()').extract_first()
                    if aval is not None:
                        if 'immediate' in aval:
                            item['Possession'] = '0'
                        elif 'availability' in aval:
                            aval = aval.split('availability ')[1]
                            item['Possession'] = dt.strftime(dt.strptime(aval, '%b %Y'), '%m/%d/%Y')
                    else:
                        item['Possession'] = '0'
                '''
                try:
                    dat = int(data['verificationDate'])/1000
                    item['listing_date'] = time.strftime('%m/%d/%Y %H:%M:%S',time.gmtime(dat))
                    item['updated_date'] = item['listing_date']
                except:
                    item['listing_date'] = dt.now().strftime('%m/%d/%Y %H:%M:%S')
                    item['updated_date'] = item['listing_date']
                '''
                if not (data['verificationDate'] == ''):
                    dat = int(data['verificationDate']) / 1000
                    item['listing_date'] = datetime.datetime.utcfromtimestamp(dat).strftime('%m/%d/%Y')
                    item['updated_date'] = item['listing_date']
                else:
                    item['listing_date'] = dt.now().strftime('%m/%d/%Y')
                    item['updated_date'] = item['listing_date']

                if 'ale' in item['txn_type']:
                    prc_pr_sf = i.xpath('.//div[contains(@class,"lbl rate")]/text()').extract_first(default='0')
                    item['price_per_sqft'] = re.findall('[0-9]+', prc_pr_sf)
                    item['price_per_sqft'] = ''.join(item['price_per_sqft'])
                else:
                    item['price_per_sqft'] = '0'

                sqf = data['size']
                # i.xpath('.//span[@class="size"]/text()').extract_first()
                try:
                    item['Bua_sqft'] = re.findall('[0-9]+', sqf)
                    item['Bua_sqft'] = ''.join(item['Bua_sqft'])
                    if item['Bua_sqft'] == '' or item['Bua_sqft'] == ' ' or item['Bua_sqft'] is None:
                        item['Bua_sqft'] = '0'
                except:
                    item['Bua_sqft'] = '0'

                age = i.xpath('.//div[@class="infoWrap"]/div[@class="listing-details"]/span[@title="old"]/span/text()').extract_first(default='0')

                if 'year' in age:
                    if '-' in age:
                        age = re.findall('[0-9]+', age.split('-')[1])[0]
                    else:
                        age = re.findall('[0-9]+', age)[0]

                if age == '' or age == ' ' or age is None:
                    age = '0'

                item['age'] = age

                item['Details'] = i.xpath('.//div[@class="otherDetails"]/text()').extract_first(default='None').split('.')[0]

                try:
                    if len(item['Building_name']) < 3 or len(item['Building_name']) > 35:
                        item['Building_name'] = 'None'
                except Exception as e:
                    print("Exception at building name", e)

                item['scraped_time'] = dt.now().strftime('%m/%d/%Y')

                if not item['Building_name'] == 'None' and not item['sublocality'] == 'None' and not item['locality'] == 'None':
                    item['address'] = item['Building_name'] + ',' + item['sublocality'] + ',' + item['locality'] + ',' + item['city']
                elif not item['sublocality'] == 'None' and not item['locality'] == 'None':
                    item['address'] = item['sublocality'] + ',' + item['locality'] + ',' + item['city']
                elif not item['Building_name'] == 'None' and not item['locality'] == 'None':
                    item['address'] = item['Building_name'] + ',' + item['locality'] + ',' + item['city']
                elif not item['locality'] == 'None':
                    item['address'] = item['locality'] + ',' + item['city']
                else:
                    item['address'] = item['city']

                if ((not item['Monthly_Rent'] == '0') and (not item['Bua_sqft'] == '0') and (not item['Building_name'] == 'None') and (not item['lat'] == '0')) or ((not item['Selling_price'] == '0') and (not item['Bua_sqft'] == '0') and (not item['Building_name'] == 'None') and (not item['lat'] == '0')) or ((not item['price_per_sqft'] == '0') and (not item['Bua_sqft'] == '0') and (not item['Building_name'] == 'None') and (not item['lat'] == '0')):
                    item['quality4'] = 1
                elif ((not item['price_per_sqft'] == '0') and (not item['Building_name'] == 'None') and (not item['lat'] == '0')) or ((not item['Selling_price'] == '0') and (not item['Bua_sqft'] == '0') and (not item['lat'] == '0')) or ((not item['Monthly_Rent'] == '0') and (not item['Bua_sqft'] == '0') and (not item['lat'] == '0')) or ((not item['Selling_price'] == '0') and (not item['Bua_sqft'] == '0') and (not item['Building_name'] == 'None')) or ((not item['Monthly_Rent'] == '0') and (not item['Bua_sqft'] == '0') and (not item['Building_name'] == 'None')):
                    item['quality4'] = 0.5
                else:
                    item['quality4'] = 0

                if (not item['mobile_lister'] == 'None') or (not item['listing_by'] == 'None') or (not item['name_lister'] == 'None'):
                    item['quality3'] = 1
                else:
                    item['quality3'] = 0

                if (not item['Launch_date'] == '0') or (not item['Possession'] == '0'):
                    item['quality2'] = 1
                else:
                    item['quality2'] = 0

                if (not item['Building_name'] == 'None') and (not item['listing_date'] == '0') and (not item['txn_type'] == 'None') and (not item['property_type'] == 'None') and ((not item['Selling_price'] == '0') or (not item['Monthly_Rent'] == '0')):
                    item['quality1'] = 1
                else:
                    item['quality1'] = 0
            except Exception as e:
                print("Exception in loop", e)
            finally:
                yield item
        try:
            pages = json.loads(response.xpath('//div[@data-listing-wrapper]/script/text()').extract_first())
            if pages is not None:
                pageno = int(response.url.split('page=')[1])
                totalpages = pages['totalPages']
                if pageno < totalpages:
                    url = response.url.split('page=')[0] + 'page=' + str(pageno + 1)
                    yield Request(url, callback=self.parse, dont_filter=True)
            elif 'cardholder' in response.body:
                pageno = int(response.url.split('page=')[1])
                url = response.url.split('page=')[0] + 'page=' + str(pageno + 1)
                yield Request(url, callback=self.parse, dont_filter=True)
        except Exception as e:
            print("Exception at pagination", e)

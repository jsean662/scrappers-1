# -*- coding: utf-8 -*-
import scrapy
from ..items import MakaanDelhirentItem
import json
import datetime
from datetime import datetime as dt
from scrapy.selector import Selector
import re
from scrapy.http import Request

class MakaanrentdelhiSpider(scrapy.Spider):
    name = "makaanRentDelhi"
    allowed_domains = ["makaan.com"]
    start_urls = [
        'https://www.makaan.com/listings?sortBy=date-desc&listingType=rent&pageType=LISTINGS_PROPERTY_URLS&cityName=Delhi&cityId=6&templateId=MAKAAN_CITY_LISTING_BUY&page=1',
    ]
    custom_settings = {
        'DEPTH_LIMIT': 5000,
        'DOWNLOAD_DELAY': 3,
    }

    def parse(self, response):
        item = MakaanDelhirentItem()
        hxs = Selector(response)
        a = hxs.xpath("//div[@class='cardholder']")

        for i in a:
            try:
                detail = i.xpath('./div[contains(@class,"cardWrapper")]/script/text()').extract_first()
                data = json.loads(detail)

                item['carpet_area'] = '0'
                item['updated_date'] = '0'
                item['management_by_landlord'] = 'None'
                item['areacode'] = '0'
                item['mobile_lister'] = '0'
                item['google_place_id'] = 'None'
                item['age'] = '0'
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

                item['platform'] = 'Makaan'

                item['data_id'] = data['id']

                item['name_lister'] = data['companyName']
                if item['name_lister'] == '':
                    item['name_lister'] = 'None'

                item['listing_by'] = data['sellerType']

                try:
                    item['mobile_lister'] = data['companyPhone']
                except:
                    item['mobile_lister'] = '0'

                item['lat'] = data['latitude']
                if item['lat'] == '':
                    item['lat'] = '0'

                item['longt'] = data['longitude']
                if item['longt'] == '':
                    item['longt'] = '0'

                item['locality'] = data['localityName']

                item['city'] = data['cityName']

                item['Building_name'] = data['fullName']
                if item['Building_name'] == '':
                    item['Building_name'] = 'None'

                item['config_type'] = data['bedrooms'] + 'BHK'

                item['txn_type'] = data['listingCategory']

                if 'Primary' in item['txn_type']:
                    item['txn_type'] = 'Sale'

                if item['txn_type'] == 'Sale' or item['txn_type'] == 'Resale':
                    item['Selling_price'] = data['price']
                    item['Monthly_Rent'] = '0'

                if 'Rental' in item['txn_type']:
                    item['Monthly_Rent'] = data['price']
                    item['Selling_price'] = '0'

                if item['Selling_price'] == '0' and item['Monthly_Rent'] == '0':
                    item['price_on_req'] = 'TRUE'
                else:
                    item['price_on_req'] = 'FALSE'

                item['Status'] = data['projectStatus']
                if item['Status'] == '' or item['Status'] is None:
                    aval = i.xpath('.//*[contains(@class,"dcol poss")]/div[1]/text()').extract_first()
                    if aval is not None:
                        if 'Immediate' not in aval:
                            item['Possession'] = dt.strftime(dt.strptime(aval, '%b %Y'), '%m/%d/%Y')
                        item['Status'] = i.xpath('.//*[contains(@class,"dcol furnishstatus")]/div[1]/text()').extract_first(default='None')
                    else:
                        item['Status'] = 'None'
                '''
                try:
                    dat = int(data['verificationDate'])/1000
                    item['listing_date'] = time.strftime('%m/%d/%Y',time.gmtime(dat))
                    item['updated_date'] = item['listing_date']
                except:
                    item['listing_date'] = dt.now().strftime('%m/%d/%Y')
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
                    prc_pr_sf = i.xpath('div[contains(@class,"cardWrapper")]/div[@class="cardLayout clearfix"]/div[@class="infoWrap"]/div[@class="headInfo"]/div[@class="priceWrap"]/div[@class="price-rate-col"]/div[@class="rate"]/span[@class="val"]/text()').extract_first()
                    item['price_per_sqft'] = re.findall('[0-9]+', prc_pr_sf)
                    item['price_per_sqft'] = ''.join(item['price_per_sqft'])
                else:
                    item['price_per_sqft'] = '0'

                sqf = i.xpath('.//span[@class="size"]/text()').extract_first()
                try:
                    item['Bua_sqft'] = re.findall('[0-9]+', sqf)
                    item['Bua_sqft'] = ''.join(item['Bua_sqft'])
                except:
                    item['Bua_sqft'] = '0'

                if 'esale' in item['txn_type']:
                    item['age'] = i.xpath('div[contains(@class,"cardWrapper")]/div[@class="cardLayout clearfix"]/div[@class="infoWrap"]/div[@class="highlight-points"]/div[@class="dcol poss"]/div[@class="val ''"]/text()').extract_first()

                item['Details'] = i.xpath('.//div[@class="otherDetails"]/text()').extract_first().split('.')[0]

                try:
                    if len(item['Building_name']) < 3 or len(item['Building_name']) > 35:
                        item['Building_name'] = 'None'
                except:
                    pass

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

                if (((not item['Monthly_Rent'] == '0') and (not item['Bua_sqft'] == '0') and (not item['Building_name'] == 'None') and (not item['lat'] == '0')) or ((not item['Selling_price'] == '0') and (not item['Bua_sqft'] == '0') and (not item['Building_name'] == 'None') and (not item['lat'] == '0')) or ((not item['price_per_sqft'] == '0') and (not item['Bua_sqft'] == '0') and (not item['Building_name'] == 'None') and (not item['lat'] == '0'))):
                    item['quality4'] = 1
                elif (((not item['price_per_sqft'] == '0') and (not item['Building_name'] == 'None') and (not item['lat'] == '0')) or ((not item['Selling_price'] == '0') and (not item['Bua_sqft'] == '0') and (not item['lat'] == '0')) or ((not item['Monthly_Rent'] == '0') and (not item['Bua_sqft'] == '0') and (not item['lat'] == '0')) or ((not item['Selling_price'] == '0') and (not item['Bua_sqft'] == '0') and (not item['Building_name'] == 'None')) or ((not item['Monthly_Rent'] == '0') and (not item['Bua_sqft'] == '0') and (not item['Building_name'] == 'None'))):
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
                try:
                    pages = json.loads(response.xpath('//div[@data-listing-wrapper]/script/text()').extract_first())
                    if pages is not None:
                        pageno = int(response.url.split('page=')[1])
                        totalpages = pages['totalPages']
                        if pageno < totalpages:
                            url = 'https://www.makaan.com/listings?sortBy=date-desc&listingType=rent&pageType=LISTINGS_PROPERTY_URLS&cityName=Delhi&cityId=6&templateId=MAKAAN_CITY_LISTING_BUY&page=' + str(pageno+1)
                            yield Request(url, callback=self.parse)
                except Exception as e:
                    print(e)
            except Exception as e:
                print(e)

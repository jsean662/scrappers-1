# -*- coding: utf-8 -*-
import scrapy
from ..items import MagicbricksrenthyderabadItem
from scrapy.spiders import Spider
from scrapy.spiders import CrawlSpider, Rule
from scrapy.selector import Selector
from scrapy.http import Request
from scrapy.http import FormRequest
from datetime import datetime as dt
from datetime import time, timedelta
from datetime import date
import re


class MagicrenthyderabadSpider(scrapy.Spider):
    name = "magicRentHyderabad"
    allowed_domains = ["magicbricks.com"]
    start_urls = [
        'http://www.magicbricks.com/property-for-rent/residential-real-estate?proptype=Multistorey-Apartment,Builder-Floor-Apartment,Penthouse,Studio-Apartment,Service-Apartment,Residential-House,Villa&cityName=Hyderabad&sortBy=mostRecent/Page-1',
    ]
    custom_settings = {
        'DEPTH_LIMIT': 10000,
        'DOWNLOAD_DELAY': 5.0,
    }

    def parse(self, response):
        # record = Selector(response)

        try:

            data = response.xpath('//div[contains(@id,"resultBlockWrapper")]')  # response.xpath('//div[@class="srpBlockWrapper"]')record.xpath('//div[@class="srpColm2"]/div[@class="proColmleft"]')
            lister = response.xpath('//div[@class="srpColm2"]')
            dates = response.xpath('//span[@class="postedBy"]')
            k = 0
            item = MagicbricksrenthyderabadItem()
            for i in data:
                try:
                    item['address'] = 'None'
                    item['areacode'] = 'None'
                    item['management_by_landlord'] = 'None'
                    item['mobile_lister'] = 'None'
                    item['lat'] = '0'
                    item['longt'] = '0'
                    item['price_per_sqft'] = '0'
                    item['Launch_date'] = '0'
                    item['Possession'] = '0'
                    item['google_place_id'] = 'None'
                    item['listing_by'] = 'None'
                    item['age'] = '0'
                    item['sublocality'] = 'None'
                    item['carpet_area'] = 'None'
                    item['scraped_time'] = dt.now().strftime('%m/%d/%Y')
                    item['Status'] = 'None'
                    item['platform'] = 'Magicbricks'
                    item['txn_type'] = 'Rent'
                    item['locality'] = 'None'
                    item['Details'] = 'None'
                    item['quality1'] = item['quality2'] = item['quality3'] = item['quality4'] = '0'

                    item['property_type'] = i.xpath('.//p[@class="proHeading"]/a/input[2]/@value').extract_first(default='Residential').strip()
                    if item['property_type'] == 'Studio Apartment' or (item['property_type'] == 'Apartment'):
                        item['config_type'] = '1RK'

                    item['city'] = response.url.split('&cityName=')[1].split('&')[0]
                    item['data_id'] = re.findall('[0-9]+', i.xpath('@id').extract_first(default='0'))[0]

                    # item['lat'] = i.xpath('.//div[@itemprop="geo"]/input[2]/@value').extract_first()
                    try:
                        lat_longt = i.xpath('.//a[@class="Rent-SeeOnMapLink"]/@onclick').extract_first(default='0').split('?')[1]
                    except:
                        pass
                    try:
                        item['lat'] = lat_longt.split('&')[0].replace('lat=', '')
                        if item['lat'] == '':
                            item['lat'] = '0'
                    except:
                        item['lat'] = '0'

                    try:
                        item['longt'] = lat_longt.split('&')[1].replace('longt=', '')
                        if item['longt'] == '':
                            item['longt'] = '0'
                    except:
                        item['longt'] = '0'

                    locality = i.xpath('.//span[contains(@id,"localityName")]/text()').extract_first(default='None').strip()
                    if locality == item['city']:
                        locality = 'None'
                    if ',' in locality:
                        l = len(locality.split(','))
                        if l >= 3:
                            item['sublocality'] = locality.split(',')[0].strip()
                            item['locality'] = locality.split(',')[1:]
                        elif l == 2 and (not locality.split(',')[1] == '' or not locality.split(',')[1] == ' '):
                            item['sublocality'] = locality.split(',')[0].strip()
                            item['locality'] = locality.split(',')[1].strip()
                        else:
                            item['sublocality'] = 'None'
                            item['locality'] = locality.split(',')[0].strip()
                    else:
                        item['locality'] = locality

                    building_name = 'projectName' + item['data_id']

                    item['Building_name'] = i.xpath('.//input[@id="' + building_name + '"]/@value').extract_first(default='None')
                    if item['Building_name'] == ' ' or item['Building_name'] == '' or item['Building_name'] is None or str(item['Building_name']).isdigit() is True:
                        item['Building_name'] = 'None'

                    item['config_type'] = i.xpath('.//input[contains(@id,"bedroomVal")]/@value').extract_first(default='None').replace('>', '').strip()
                    if item['config_type'] == 'None' or item['config_type'] == '0' or item['config_type'] == '':
                        item['config_type'] = 'None'
                    else:
                        item['config_type'] += 'BHK'

                    if item['property_type'] == 'Studio Apartment':
                        item['config_type'] = '1RK'

                    if item['config_type'] == 'BHK':
                        item['config_type'] = 'None'

                    item['Selling_price'] = '0'

                    price = i.xpath('.//div[@class="proPrice"]/span[1]/text()').extract_first(default='0').strip()

                    if 'Lac' in price:
                        price = float(price.replace("Lac", "")) * 100000
                        item['Monthly_Rent'] = str(price)
                    elif 'Call for Price' in price:
                        item['Monthly_Rent'] = '0'
                    else:
                        price = price.replace(",", "")
                        item['Monthly_Rent'] = str(eval(price))

                    if item['Selling_price'] == '0' and item['Monthly_Rent'] == '0':
                        item['price_on_req'] = 'true'
                    else:
                        item['price_on_req'] = 'false'
                    # item['carpet_area'] = 'None'

                    item['listing_by'] = i.xpath('.//input[contains(@id,"userType")]/@value').extract_first(default='None')
                    # list_by = i.xpath('.//div[@class="proAgentWrap"]/div[1]/div[1]/div[1]/text()').extract_first()
                    # if 'Agent' in list_by:
                    #     item['listing_by'] = 'Agent'
                    # elif 'Owner' in list_by:
                    #     item['listing_by'] = 'Owner'
                    # else:
                    #     item['listing_by'] = 'None'

                    item['name_lister'] = i.xpath('.//div[@class="comNameElip"]/text()').extract_first(default='None').replace('\n',' ').strip()
                    if 'null' in item['name_lister']:
                        item['name_lister'] = 'None'

                    try:
                        sqf = i.xpath('.//input[contains(@id,"propertyArea")]/@value').extract_first(default='0').strip()
                        # i.xpath('.//div[@class="proDetailsRow proDetailsRowListing proDetailsRowRent"]/div[1]/ul/li[1]/span/text()').extract_first()
                        if 'sqft' in sqf:
                            item['Bua_sqft'] = re.findall('[0-9]+', sqf)
                        elif 'kottah' in sqf:
                            item['Bua_sqft'] = re.findall('[0-9]+', sqf)
                            item['Bua_sqft'] = str(eval(item['Bua_sqft'][0]) * 720)
                        elif 'acre' in sqf:
                            item['Bua_sqft'] = re.findall('[0-9]+', sqf)
                            item['Bua_sqft'] = str(eval(item['Bua_sqft'][0]) * 43560)
                        else:
                            item['Bua_sqft'] = "0"
                    except:
                        item['Bua_sqft'] = "0"

                    try:
                        status = i.xpath('.//div[@class="proDetailsRow proDetailsRowListing proDetailsRowRent"]/div[2]/text()').extract()[1].replace('\n', ' ')
                    except:
                        status = 'Ready to Move'

                    item['Status'] = i.xpath('.//input[contains(@id,"furnshingStatus")]/@value').extract_first(default='None')

                    if ',' in status:
                        item['Possession'] = 0
                    else:
                        status = status.split('from ')[1].strip()
                        status = status.replace("'", ' ')
                        item['Possession'] = dt.strftime(dt.strptime(status, '%b %y'), '%m/%d/%y')
                        ''' if 'Available on' in status:
                             yr = re.findall('[0-9]+', status)[0]
                             if 'Jan' in status:
                                 item['Possession'] = '01/01/' + yr
                             if 'Feb' in status:
                                 item['Possession'] = '01/02/' + yr
                             if 'Mar' in status:
                                 item['Possession'] = '01/03/' + yr
                             if 'Apr' in status:
                                 item['Possession'] = '01/04/' + yr
                             if 'May' in status:
                                 item['Possession'] = '01/05/' + yr
                             if 'Jun' in status:
                                 item['Possession'] = '01/06/' + yr
                             if 'Jul' in status:
                                 item['Possession'] = '01/07/' + yr
                             if 'Aug' in status:
                                 item['Possession'] = '01/08/' + yr
                             if 'Sep' in status:
                                 item['Possession'] = '01/09/' + yr
                             if 'Oct' in status:
                                 item['Possession'] = '01/10/' + yr
                             if 'Nov' in status:
                                 item['Possession'] = '01/11/' + yr
                             if 'Dec' in status:
                                 item['Possession'] = '01/12/' + yr '''

                    try:
                        det = i.xpath('.//div[contains(@class,"showOneLilner")]/text()').extract()
                        if not det:
                            det = 'None'
                        else:
                            for dc in range(0, len(det)):
                                det[dc] = det[dc].strip().replace('\n', '')
                        item['Details'] = det
                    except Exception as e:
                        print(e)
                        item['Details'] = 'None'
                    # str(i.xpath('div[2]/div[1]/ul/li[2]/text()').extract_first())+' '+str(i.xpath('div[2]/div[1]/ul/li[3]/text()').extract_first())+' '+str(i.xpath('div[2]/div[1]/ul/li[4]/text()').extract_first())+' '+str(i.xpath('div[2]/div[1]/ul/li[5]/text()').extract_first())

                    day = dates.xpath('text()').extract_first(default='0').strip()
                    day = day.replace("Posted: ", "").replace("Posted ", "").strip()

                    if 'Today' in day:
                        item['listing_date'] = dt.now().strftime('%m/%d/%Y')
                    elif 'Yesterday' in day:
                        item['listing_date'] = str((date.today() - timedelta(days=1)).month) + "/" + str((date.today() - timedelta(days=1)).day) + "/" + str((date.today() - timedelta(days=1)).year)
                    elif 'th' in day:
                        day = day.replace("th", "")
                        day = dt.strftime(dt.strptime(day, '%d %b'), '%m/%d') + '/' + str(date.today().year)
                        item['listing_date'] = day
                    elif 'st' in day:
                        day = day.replace("st", "")
                        day = dt.strftime(dt.strptime(day, '%d %b'), '%m/%d') + '/' + str(date.today().year)
                        item['listing_date'] = day
                    elif 'rd' in day:
                        day = day.replace("rd", "")
                        day = dt.strftime(dt.strptime(day, '%d %b'), '%m/%d') + '/' + str(date.today().year)
                        item['listing_date'] = day
                    elif 'nd' in day:
                        day = day.replace("nd", "")
                        day = dt.strftime(dt.strptime(day, '%d %b'), '%m/%d') + '/' + str(date.today().year)
                        item['listing_date'] = day
                    item['updated_date'] = item['listing_date']

                    if item['sublocality'] == '' or item['sublocality'] == ' ' or item['sublocality'] == ',' or item['sublocality'] == '.':
                        item['sublocality'] = 'None'
                    if item['locality'] == '' or item['locality'] == ' ' or item['locality'] == ',' or item['locality'] == '.':
                        item['locality'] = 'None'

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
                    print(e)
                finally:
                    yield item
        except Exception as e:
            print(e)

        pagecount = int(response.xpath('//span[@id="pageCount"]/text()').extract_first(default='0.0').split('.')[0])
        pageno = int(response.url.split('Page-')[1])

        if pagecount == 0 or pagecount is None:
            if 'resultBlockWrapper' in str(response.body):
                url = response.url.split(str(pageno))[0] + str(pageno + 1)
                # print(url)
                yield Request(url, callback=self.parse, dont_filter=True)
        else:
            if pageno < pagecount:
                url = response.url.split(str(pageno))[0] + str(pageno + 1)
                # print(url)
                yield Request(url, callback=self.parse, dont_filter=True)

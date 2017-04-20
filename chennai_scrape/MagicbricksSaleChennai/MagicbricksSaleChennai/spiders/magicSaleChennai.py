# -*- coding: utf-8 -*-
import scrapy
from ..items import MagicbrickssalechennaiItem
from scrapy.selector import Selector
from scrapy.http import Request
import datetime
from datetime import datetime as dt
import re

class MagicsalechennaiSpider(scrapy.Spider):
    name = "magicSaleChennai"
    allowed_domains = ["magicbricks.com"]
    start_urls = [
        'http://www.magicbricks.com/property-for-sale/residential-real-estate?proptype=Multistorey-Apartment,Builder-Floor-Apartment,Penthouse,Studio-Apartment,Residential-House,Villa&cityName=Chennai&sortBy=mostRecent/Page-1',
    ]
    custom_settings = {
        'DEPTH_LIMIT': 10000,
        'DOWNLOAD_DELAY': 3.0}

    def parse(self, response):
        try:
            record = Selector(response)
            item = MagicbrickssalechennaiItem()

            data = record.xpath('//div[contains(@id,"resultBlockWrapper")]')
            # data = record.xpath('//div[@class="srcShadow animDef "]')
            for i in data:

                try:

                    item['name_lister'] = 'None'
                    item['Details'] = 'None'
                    item['listing_by'] = 'None'
                    item['address'] = 'None'
                    item['sublocality'] = 'None'
                    item['age'] = '0'
                    item['google_place_id'] = 'None'
                    item['lat'] = '0'
                    item['longt'] = '0'
                    item['Possession'] = '0'
                    item['Launch_date'] = '0'
                    item['mobile_lister'] = 'None'
                    item['areacode'] = 'None'
                    item['management_by_landlord'] = 'None'
                    item['Monthly_Rent'] = '0'
                    item['price_per_sqft'] = '0'
                    item['Status'] = 'None'
                    item['scraped_time'] = dt.now().strftime('%m/%d/%Y')
                    item['city'] = response.url.split('&cityName=')[1].split('&')[0]
                    item['locality'] = 'None'

<<<<<<< HEAD
                    ids = i.xpath('@id').extract_first()
                    item['data_id'] = re.findall('[0-9]+', ids)[0]

                    building_name = 'projectName' + item['data_id']

                    item['Building_name'] = i.xpath('.//input[@id="' + building_name + '"]/@value').extract_first(default='None')
                    if item['Building_name'] == ' ' or item['Building_name'] == '' or item[
                        'Building_name'] is None or str(item['Building_name']).isdigit() is True:
                        item['Building_name'] = 'None'

                    try:
                        item['lat'] = \
                        i.xpath('./*//div[@class="iconMap"]/a/@onclick').extract_first(default=0).split('lat=')[
                            1].split('&')[0]
=======
                    item['Building_name'] = i.xpath('.//input[contains(@id,"projectName")]/@value').extract_first()
                    if item['Building_name'] == ' ' or item['Building_name'] == '' or item['Building_name'] is None:
                        item['Building_name'] = 'None'

                    try:
                        item['lat'] = i.xpath('*//div[@class="iconMap"]/a/@onclick').extract_first(default=0).split('lat=')[1].split('&')[0]
>>>>>>> ec62c69e8c728b37e8eebf8cc672512203d9567f
                        if item['lat'] == '' or item['lat'] == ' ':
                            item['lat'] = '0'
                    except Exception as e:
                        print(e)
                        item['lat'] = '0'

                    try:
<<<<<<< HEAD
                        item['longt'] = \
                        i.xpath('./*//div[@class="iconMap"]/a/@onclick').extract_first(default=0).split('longt=')[
                            1].split('&')[0]
=======
                        item['longt'] = i.xpath('*//div[@class="iconMap"]/a/@onclick').extract_first(default=0).split('longt=')[1].split('&')[0]
>>>>>>> ec62c69e8c728b37e8eebf8cc672512203d9567f
                        if item['longt'] == '' or item['longt'] == ' ':
                            item['longt'] = '0'
                    except Exception as e:
                        print(e)
                        item['longt'] = '0'

                    item['platform'] = 'Magicbricks'
                    item['carpet_area'] = '0'

<<<<<<< HEAD
                    item['config_type'] = i.xpath('.//input[contains(@id,"bedroomVal")]/@value').extract_first(
                        default='None').replace('>', '').strip()
                    item['config_type'] += 'BHK'

                    item['property_type'] = i.xpath('.//input[contains(@id,"propertyVal")]/@value').extract_first(
                        default='Residential').strip()
                    if 'Studio Apartment' in item['property_type']:
                        item['config_type'] = '1RK'

                    if item['config_type'] == 'BHK' or item['config_type'] == '' or item['config_type'] == ' ' or item[
                        'config_type'] == '0BHK' or item['config_type'] == 'NoneBHK':
=======
                    ids = i.xpath('@id').extract_first()
                    item['data_id'] = re.findall('[0-9]+', ids)[0]

                    item['config_type'] = i.xpath('.//input[contains(@id,"bedroomVal")]/@value').extract_first(default='None').replace('>', '')
                    item['config_type'] += 'BHK'

                    item['property_type'] = i.xpath('.//input[contains(@id,"propertyVal")]/@value').extract_first()
                    if 'Studio Apartment' in item['property_type']:
                        item['config_type'] = '1RK'

                    if item['config_type'] == 'BHK' or item['config_type'] == '' or item['config_type'] == ' ':
>>>>>>> ec62c69e8c728b37e8eebf8cc672512203d9567f
                        item['config_type'] = 'None'

                    try:
                        sqf = i.xpath('.//input[contains(@id,"propertyArea")]/@value').extract_first()
                        if 'sqft' in sqf:
                            item['Bua_sqft'] = re.findall('[0-9]+', sqf)
                        elif 'kottah' in sqf:
                            item['Bua_sqft'] = re.findall('[0-9]+', sqf)
                            item['Bua_sqft'] = str(eval(item['Bua_sqft'][0]) * 720)
                        elif 'sqm':
                            item['Bua_sqft'] = re.findall('[0-9]+', sqf)
                            item['Bua_sqft'] = str(eval(item['Bua_sqft'][0]) * 10)
                        elif 'sqyrd':
                            item['Bua_sqft'] = re.findall('[0-9]+', sqf)
                            item['Bua_sqft'] = str(eval(item['Bua_sqft'][0]) * 9)
                        else:
                            item['Bua_sqft'] = '0'
                    except:
                        item['Bua_sqft'] = '0'

<<<<<<< HEAD
                    locality = i.xpath('.//span[contains(@id,"localityName")]/text()').extract_first(
                        default='None').strip()
                    if ',' in locality:
                        l = len(locality.split(','))
                        if l >= 3:
                            item['sublocality'] = locality.split(',')[0].strip()
                            item['locality'] = locality.split(',')[1:]
                        elif l == 2 and (not locality.split(',')[1] == '' or locality.split(',')[1] == ' '):
                            item['sublocality'] = locality.split(',')[0].strip()
                            item['locality'] = locality.split(',')[1].strip()
                        else:
                            item['sublocality'] = 'None'
                            item['locality'] = locality.split(',')[0].strip()
                    else:
                        item['locality'] = locality

                    if item['sublocality'] == '' or item['sublocality'] == ' ' or item['sublocality'] == ',' or item[
                        'sublocality'] == '.':
                        item['sublocality'] = 'None'
                    if item['locality'] == '' or item['locality'] == ' ' or item['locality'] == ',' or item[
                        'locality'] == '.':
                        item['locality'] = 'None'

                    socOrStat = i.xpath('.//div/div/div[1]/div[5]/div/div[2]/div[1]/text()').extract_first(
                        default='None').strip()
                    # print(socOrStat)
                    stat = ''
                    if 'Society' in socOrStat:
                        stat = i.xpath('.//div/div/div[1]/div[5]/div/div[2]/div[5]/text()').extract_first(
                            default='None')
                    elif 'Non' in socOrStat:
                        stat = i.xpath('.//div/div/div[1]/div[5]/div/div[2]/div[3]/text()').extract_first(
                            default='None')
=======
                    locality = i.xpath('.//span[contains(@id,"localityName")]/text()').extract_first(default='None')
                    if ',' in locality:
                        l = len(locality.split(','))
                        if l >= 3:
                            item['sublocality'] = locality.split(',')[0]
                            item['locality'] = locality.split(',')[1:]
                        elif l == 2 and (not locality.split(',')[1] == '' or locality.split(',')[1] == ' '):
                            item['sublocality'] = locality.split(',')[0]
                            item['locality'] = locality.split(',')[1]
                        else:
                            item['sublocality'] = 'None'
                            item['locality'] = locality.split(',')[0]
                    else:
                        item['locality'] = locality

                    if item['sublocality'] == '' or item['sublocality'] == ' ' or item['sublocality'] == ',' or item['sublocality'] == '.':
                        item['sublocality'] = 'None'
                    if item['locality'] == '' or item['locality'] == ' ' or item['locality'] == ',' or item['locality'] == '.':
                        item['locality'] = 'None'

                    socOrStat = i.xpath('.//div/div/div[1]/div[5]/div/div[2]/div[1]/text()').extract_first(default='None')
                    # print(socOrStat)
                    stat = ''
                    if 'Society' in socOrStat:
                        stat = i.xpath('.//div/div/div[1]/div[5]/div/div[2]/div[5]/text()').extract_first(default='None')
                    elif 'Non' in socOrStat:
                        stat = i.xpath('.//div/div/div[1]/div[5]/div/div[2]/div[3]/text()').extract_first(default='None')
>>>>>>> ec62c69e8c728b37e8eebf8cc672512203d9567f
                        # stat = (''.join(stat)).replace('\n', '')

                    try:
                        if 'Under' in stat:
                            item['Status'] = 'Under Construction'
<<<<<<< HEAD
                            poss = stat.split('Ready by ')[1].replace("'", "").replace(')', '').replace('\n',
                                                                                                        '').replace(
                                ', Freehold', '').replace('. Freehold', '').replace(', Leasehold', '').replace(
                                '. Leasehold', '')
=======
                            poss = stat.split('Ready by ')[1].replace("'", "").replace(')', '').replace('\n', '').replace(', Freehold', '').replace('. Freehold', '').replace(', Leasehold', '').replace('. Leasehold', '')
>>>>>>> ec62c69e8c728b37e8eebf8cc672512203d9567f
                            # print("POSSESSION: ", poss)
                            item['Possession'] = dt.strftime(dt.strptime(poss, '%b %y'), '%m/%d/%Y')
                        else:
                            item['Status'] = 'Ready To Move'
                    except:
                        item['Status'] = 'Ready to move'
                        item['Possession'] = '0'

                    if item['Status'] == '' or item['Status'] == ' ' or item['Status'] is None:
                        item['Status'] = 'None'

<<<<<<< HEAD
                    item['Details'] = i.xpath(
                        './/div/div/div[1]/div[4]/div/div[2]/div[@class="labValu"][last()]/text()').extract_first(
                        default='None').strip().replace('\n', '')
=======
                    item['Details'] = i.xpath('.//div/div/div[1]/div[4]/div/div[2]/div[@class="labValu"][last()]/text()').extract_first(default='None').strip().replace('\n', '')
>>>>>>> ec62c69e8c728b37e8eebf8cc672512203d9567f

                    if item['Details'] == '' or item['Details'] == ' ':
                        item['Details'] = 'None'

<<<<<<< HEAD
                    price = i.xpath(
                        './/div[@class="sLB"]/div[@class="SRPriceB"]/span[contains(@id,"pricePropertyVal")]/text()').extract_first()
                    # print("PRICE: ", price)
                    if price is None:
                        price = i.xpath('.//span[contains(@id,"sqrFtPriceField")]/text()').extract_first()
                        # price = ''.join(re.findall('[0-9]+', price))
                        # print("PRICE: ", price)
                    if price is not None:
=======
                    price = i.xpath('.//div[@class="sLB"]/div[@class="SRPriceB"]/span[contains(@id,"pricePropertyVal")]/text()').extract_first()
                    # print("PRICE: ", price)
                    if price == None:
                        price = i.xpath('.//span[contains(@id,"sqrFtPriceField")]/text()').extract_first()
                        # price = ''.join(re.findall('[0-9]+', price))
                        # print("PRICE: ", price)
                    if not price == None:
>>>>>>> ec62c69e8c728b37e8eebf8cc672512203d9567f
                        if 'Lac' in price:
                            item['Selling_price'] = str(float(price.split()[0]) * 100000)
                        elif 'Cr' in price:
                            item['Selling_price'] = str(float(price.split()[0]) * 10000000)
                        else:
                            item['Selling_price'] = '0'
                        if item['Selling_price'] == 'None':
                            item['Selling_price'] = '0'
                    else:
                        item['Selling_price'] = '0'

                    if item['Selling_price'] == '0':
                        item['price_on_req'] = 'true'
                    else:
                        item['price_on_req'] = 'false'

                    try:
<<<<<<< HEAD
                        sqft_per = i.xpath(
                            './/div[@class="sLB"]/div[@class="SRPPS"]/span[contains(@id,"sqrFtPriceField")]/text()').extract_first()
=======
                        sqft_per = i.xpath('.//div[@class="sLB"]/div[@class="SRPPS"]/span[contains(@id,"sqrFtPriceField")]/text()').extract_first()
>>>>>>> ec62c69e8c728b37e8eebf8cc672512203d9567f
                        if sqft_per:
                            item['price_per_sqft'] = ''.join(re.findall('[0-9]+', sqft_per))
                        else:
                            item['price_per_sqft'] = '0'
                        if 'kottah' in sqft_per:
                            item['price_per_sqft'] = str(eval(item['price_per_sqft']) / 720)

                    except:
                        item['price_per_sqft'] = '0'

                    try:
<<<<<<< HEAD
                        item['listing_by'] = i.xpath('.//*[contains(@id,"userType")]/@value').extract_first(
                            default='None')
=======
                        item['listing_by'] = i.xpath('.//*[contains(@id,"userType")]/@value').extract_first(default='None')
>>>>>>> ec62c69e8c728b37e8eebf8cc672512203d9567f
                        # if 'Agent' in lister:
                        #     item['listing_by'] = 'Agent'
                        # elif 'Owner' in lister:
                        #     item['listing_by'] = 'Owner'
                        # elif 'Builder' in lister:
                        #     item['listing_by'] = 'Builder'
<<<<<<< HEAD
                        lister = i.xpath('.//div/div/div[3]/div[4]/div/div[1]/div[2]/text()').extract_first(
                            default='None').strip()
=======
                        lister = i.xpath('.//div/div/div[3]/div[4]/div/div[1]/div[2]/text()').extract_first(default='None').strip()
>>>>>>> ec62c69e8c728b37e8eebf8cc672512203d9567f
                        item['name_lister'] = lister.split(':')[1].strip()

                    except Exception as e:
                        print(e)

<<<<<<< HEAD
                    item['txn_type'] = 'Sale'
                    # i.xpath('.//div/input[contains(@id,"transactionType")]/@value').extract_first(default='Sale')

                    day = i.xpath('.//div/input[contains(@id,"createDate")]/@value').extract_first(default='0').strip()
=======
                    item['txn_type'] = i.xpath('.//div/input[contains(@id,"transactionType")]/@value').extract_first()

                    day = i.xpath('.//div/input[contains(@id,"createDate")]/@value').extract_first()
>>>>>>> ec62c69e8c728b37e8eebf8cc672512203d9567f
                    try:
                        item['listing_date'] = dt.strftime(dt.strptime(day, "%b %d, '%y"), '%m/%d/%Y')
                        item['updated_date'] = item['listing_date']
                    except:
                        item['listing_date'] = 0
                        item['updated_date'] = item['listing_date']

<<<<<<< HEAD
                    if not item['Building_name'] == 'None' and not item['sublocality'] == 'None' and not item[
                        'locality'] == 'None':
                        item['address'] = item['Building_name'] + ',' + item['sublocality'] + ',' + item[
                            'locality'] + ',' + item['city']
=======
                    if not item['Building_name'] == 'None' and not item['sublocality'] == 'None' and not item['locality'] == 'None':
                        item['address'] = item['Building_name'] + ',' + item['sublocality'] + ',' + item['locality'] + ',' + item['city']
>>>>>>> ec62c69e8c728b37e8eebf8cc672512203d9567f
                    elif not item['sublocality'] == 'None' and not item['locality'] == 'None':
                        item['address'] = item['sublocality'] + ',' + item['locality'] + ',' + item['city']
                    elif not item['Building_name'] == 'None' and not item['locality'] == 'None':
                        item['address'] = item['Building_name'] + ',' + item['locality'] + ',' + item['city']
                    elif not item['locality'] == 'None':
                        item['address'] = item['locality'] + ',' + item['city']
                    else:
                        item['address'] = item['city']

<<<<<<< HEAD
                    if ((not item['Bua_sqft'] == '0') and (not item['Building_name'] == 'None') and (
                    not item['lat'] == '0')) or (
                                (not item['Selling_price'] == '0') and (not item['Bua_sqft'] == '0') and (
                        not item['Building_name'] == 'None') and (not item['lat'] == '0')) or (
                                (not item['price_per_sqft'] == '0') and (not item['Bua_sqft'] == '0') and (
                        not item['Building_name'] == 'None') and (not item['lat'] == '0')):
                        item['quality4'] = 1
                    elif ((not item['price_per_sqft'] == '0') and (not item['Building_name'] == 'None') and (
                    not item['lat'] == '0')) or (
                            (not item['Selling_price'] == '0') and (not item['Bua_sqft'] == '0') and (
                    not item['lat'] == '0')) or ((not item['Bua_sqft'] == '0') and (not item['lat'] == '0')) or (
                            (not item['Selling_price'] == '0') and (not item['Bua_sqft'] == '0') and (
                    not item['Building_name'] == 'None')) or (
                        (not item['Bua_sqft'] == '0') and (not item['Building_name'] == 'None')):
                        item['quality4'] = 0.5
                    else:
                        item['quality4'] = 0
                    if (not item['Building_name'] == 'None') and (not item['listing_date'] == '0') and (
                    not item['txn_type'] == 'None') and (not item['property_type'] == 'None') and (
                    not item['Selling_price'] == '0'):
=======
                    if (((not item['Bua_sqft'] == '0') and (not item['Building_name'] == 'None') and (not item['lat'] == '0')) or ((not item['Selling_price'] == '0') and (not item['Bua_sqft'] == '0') and (not item['Building_name'] == 'None') and (not item['lat'] == '0')) or ((not item['price_per_sqft'] == '0') and (not item['Bua_sqft'] == '0') and (not item['Building_name'] == 'None') and (not item['lat'] == '0'))):
                        item['quality4'] = 1
                    elif (((not item['price_per_sqft'] == '0') and (not item['Building_name'] == 'None') and (not item['lat'] == '0')) or ((not item['Selling_price'] == '0') and (not item['Bua_sqft'] == '0') and (not item['lat'] == '0')) or ((not item['Bua_sqft'] == '0') and (not item['lat'] == '0')) or ((not item['Selling_price'] == '0') and (not item['Bua_sqft'] == '0') and (not item['Building_name'] == 'None')) or ((not item['Bua_sqft'] == '0') and (not item['Building_name'] == 'None'))):
                        item['quality4'] = 0.5
                    else:
                        item['quality4'] = 0
                    if ((not item['Building_name'] == 'None') and (not item['listing_date'] == '0') and (not item['txn_type'] == 'None') and (not item['property_type'] == 'None') and ((not item['Selling_price'] == '0'))):
>>>>>>> ec62c69e8c728b37e8eebf8cc672512203d9567f
                        item['quality1'] = 1
                    else:
                        item['quality1'] = 0

<<<<<<< HEAD
                    if (not item['Launch_date'] == '0') and (not item['Possession'] == '0'):
=======
                    if ((not item['Launch_date'] == '0') and (not item['Possession'] == '0')):
>>>>>>> ec62c69e8c728b37e8eebf8cc672512203d9567f
                        item['quality2'] = 1
                    else:
                        item['quality2'] = 0

<<<<<<< HEAD
                    if (not item['mobile_lister'] == 'None') or (not item['listing_by'] == 'None') or (
                    not item['name_lister'] == 'None'):
                        item['quality3'] = 1
                    else:
                        item['quality3'] = 0
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
=======
                    if ((not item['mobile_lister'] == 'None') or (not item['listing_by'] == 'None') or (
                    not item['name_lister'] == 'None')):
                        item['quality3'] = 1
                    else:
                        item['quality3'] = 0
                    yield item
                except Exception as e:
                    print(e)

        except Exception as e:
            print(e)
        noresult = "Couldn't find the property you were looking for? Set a Property Alert!"

        if 'resultBlockWrapper' in str(response.body):
            pageno = int(response.url.split('Page-')[1])
            url = 'http://www.magicbricks.com/property-for-sale/residential-real-estate?proptype=Multistorey-Apartment,Builder-Floor-Apartment,Penthouse,Studio-Apartment,Residential-House,Villa&cityName=Chennai&sortBy=mostRecent/Page-' + str(pageno+1)
            # print(url)
            yield Request(url, callback=self.parse, dont_filter=True)
        # pagecount = int(response.xpath('//span[@id="pageCount"]/text()').extract_first(default='0.0').split('.')[0])
        # pageNo = int(response.url.split('Page-')[1])
        #
        # if pagecount == 0 or pagecount is None:
        #     pass
        # else:
        #     if pageNo < pagecount:
        #         url = 'http://www.magicbricks.com/property-for-sale/residential-real-estate?proptype=Multistorey-Apartment,Builder-Floor-Apartment,Penthouse,Studio-Apartment,Residential-House,Villa&cityName=Delhi-NCR&sortBy=mostRecent/Page-' + str(pageNo + 1)
        #         # print(url)
        #         yield Request(url, callback=self.parse)
>>>>>>> ec62c69e8c728b37e8eebf8cc672512203d9567f

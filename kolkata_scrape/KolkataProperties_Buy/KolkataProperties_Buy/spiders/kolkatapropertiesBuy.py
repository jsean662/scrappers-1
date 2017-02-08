# -*- coding: utf-8 -*-
import scrapy
from scrapy.selector import Selector
from scrapy.http import Request
from ..items import KolkatapropertiesBuyItem
import re
from datetime import datetime as dt
from dateutil.relativedelta import relativedelta


class KolkatapropertiesbuySpider(scrapy.Spider):
    name = "kolkatapropertiesSaleKolkata"
    allowed_domains = ["kolkataproperties.in"]
    start_urls = [
        'http://www.kolkataproperties.in/search_results.php?buy=yes',
    ]
    custom_settings = {
        'DEPTH_LIMIT': 5000,
        'DOWNLOAD_DELAY': 3,
    }
    item = KolkatapropertiesBuyItem()

    def parse(self, response):
        try:

            error = 'Database Error: You have an error in your SQL syntax; check the manual that corresponds to your MySQL server version for the right syntax to use near'

            if error not in str(response.body):

                record = Selector(response)
                data = record.xpath('//div[contains(@class,"col-md-4")]')
                txn_type = build_name = ''

                for i in data:

                    try:
                        proptype = i.xpath('.//div/a[1]/h4/text()').extract_first()
                        if 'Land' in proptype:
                            continue
                        data_id = i.xpath('.//div/a[1]/@href').extract_first()
                        locality = i.xpath('.//div[@class="property_content"]/h4/span/text()').extract_first()

                        if ',' in locality:
                            build_name = locality.split(',')[0]
                            locality = locality.split(',')[1]

                        if 'new' in data_id:
                            txn_type = 'Sale'
                        else:
                            txn_type = 'Resale'
                        # print(data_id)
                        # self.item['data_id'] = data_id.split('=')[1]

                        url = 'http://www.kolkataproperties.in/' + data_id

                        request = Request(url, callback=self.parse1, dont_filter=True)
                        request.meta['Building_name'] = build_name
                        request.meta['locality'] = locality
                        request.meta['txn_type'] = txn_type

                        yield request
                    except Exception as e:
                        print(e)

                next_url = 'http://www.kolkataproperties.in/' + response.xpath('//a[@id="next"]/@href').extract_first()
                yield Request(next_url, callback=self.parse)
        except Exception as ex:
            print(ex)


    def parse1(self, response):
        Bua_sqft = response.xpath('//nav[@class="description_text"]/p[3]/span/text()').extract_first()
        Bua_sqft = re.findall('[0-9]+', Bua_sqft)

        price_check = 0
        for sq in Bua_sqft:
            try:

                self.item['Selling_price'] = '0'
                self.item['Possession'] = '0'
                self.item['Status'] = 'None'
                self.item['carpet_area'] = '0'
                self.item['management_by_landlord'] = 'None'
                self.item['areacode'] = 'None'
                self.item['mobile_lister'] = 'None'
                self.item['google_place_id'] = 'None'
                self.item['Launch_date'] = '0'
                self.item['age'] = 'None'
                self.item['address'] = 'None'
                self.item['price_on_req'] = 'false'
                self.item['Details'] = 'None'
                self.item['Monthly_Rent'] = '0'
                self.item['sublocality'] = 'None'
                self.item['price_per_sqft'] = '0'
                self.item['city'] = 'Kolkata'
                self.item['platform'] = 'KolkataProperties'
                self.item['listing_by'] = 'None'
                self.item['name_lister'] = 'None'
                self.item['txn_type'] = response.meta['txn_type']
                self.item['Building_name'] = response.meta['Building_name']
                self.item['locality'] = response.meta['locality']


                try:
                    geo = response.xpath('//*[@id="z_item"]/div[9]/div/div/div/script[1]/text()').extract_first().split(');')[0].split('LatLng(')

                    self.item['lat'] = geo[1].split(',')[0]
                    self.item['longt'] = geo[1].split(',')[1]
                except Exception as exc:
                    self.item['lat'] = self.item['longt'] = '0'
                    pass

                self.item['data_id'] = response.xpath('//*[@id="z_item"]/div[2]/div/section/div/div[1]/nav/p[1]/span/text()').extract()  # response.url.split('=')[1]

                dat = response.xpath('//nav[@class="description_text"]/p[2]/span/text()').extract_first() # response.xpath('//li[@class="noPrint"]/time/@datetime').extract_first().replace('Z', '')

                self.item['listing_date'] = dt.strftime(dt.strptime(dat, '%d-%b-%y'), '%m/%d/%Y %H:%M:%S')

                self.item['updated_date'] = self.item['listing_date']

                conf = response.xpath('//nav[@class="description_text"]/p[3]/text()').extract_first()
                '''bed = re.findall('[0-9]', conf)
                if bed:
                    self.item['config_type'] = bed[0] + 'BHK'
                if not bed:
                    self.item['config_type'] = 'None'
                '''

                try:
                    address = response.xpath('//nav[@class="description_text"]/p[4]/span/text()').extract()
                    t = 0
                    if self.item['locality'] in address:
                        for f in address:
                            if self.item['locality'] in f:
                                self.item['sublocality'] = address[t + 1]
                                break
                            t += 1
                    self.item['address'] = address
                except:
                    self.item['address'] = 'Kolkata'
                    self.item['sublocality'] = 'None'

                prop_type = response.xpath('//*[@id="z_item"]/section/div/a/h1/text()').extract_first()

                if 'house' in conf.lower():
                    self.item['property_type'] = 'House'
                    self.item['Building_name'] = 'None'
                elif 'office' in conf.lower():
                    self.item['property_type'] = 'Office'
                else:
                    self.item['property_type'] = 'Residential'

                try:
                    price_on_re = response.xpath('//div[@class="price_tag"]/text()').extract()
                    if 'On Request' in price_on_re:
                        self.item['price_on_req'] = 'TRUE'
                        self.item['Selling_price'] = self.item['Monthly_Rent'] = '0'
                    else:
                        self.item['price_on_req'] = 'FALSE'
                        if price_check == 0:
                            price = response.xpath('//*[@name="price"]/@value').extract_first()
                        elif price_check == 1:
                            price = response.xpath('//*[@id="z_itemprice_max_"]/@value').extract_first()

                        if 'ale' in self.item['txn_type']:
                            self.item['Selling_price'] = price
                            '''if 'la' in price:
                                price = price.split(' la')[0]
                                if (not '-' in price):
                                    self.item['Selling_price'] = str(float(price.split(' ')[0]) * 100000)
                                elif ('-' in price):
                                    self.item['Selling_price'] = str(float(price.split('-')[-1]) * 100000)
                            if 'crore' in price.lower():
                                price = price.split(' crore')[0]
                                if (not '-' in price):
                                    self.item['Selling_price'] = str(float(price.split(' ')[0]) * 10000000)
                                elif ('-' in price):
                                    self.item['Selling_price'] = str(float(price.split('-')[-1]) * 10000000)'''
                        if 'Rent' in self.item['txn_type']:
                            self.item['Monthly_Rent'] = price
                            '''if 'la' in price:
                                price = price.split(' lakh')[0]
                                if (not '-' in price):
                                    self.item['Monthly_Rent'] = str(float(price.split('-')[0]) * 100000)
                                elif ('-' in price):
                                    self.item['Monthly_Rent'] = str(float(price.split('-')[-1]) * 100000)
                            if 'crore' in price:
                                price = price.split(' crore')[0]
                                if (not '-' in price):
                                    self.item['Monthly_Rent'] = str(float(price.split('-')[0]) * 10000000)
                                elif ('-' in price):
                                    self.item['Monthly_Rent'] = str(float(price.split('-')[-1]) * 10000000)'''
                except:
                    pass

                self.item['price_per_sqft'] = 0

                try:
                    poss = response.xpath('//h4[contains(text(),"Possession ")]/text()').extract_first()
                except:
                    poss = 'None'
                if 'Immediate' in poss:
                    self.item['Possession'] = dt.today().strftime('%m/%d/%Y %H:%M:%S')
                    self.item['Status'] = 'Ready to move'
                else:
                    self.item['Possession'] = '0'
                    self.item['Status'] = 'Under Construction'

                try:
                    self.item['Bua_sqft'] = Bua_sqft[price_check]
                except:
                    self.item['Bua_sqft'] = '0'

                if 'esale' in self.item['txn_type']:
                    try:
                        age = response.xpath('//h4[contains(text(),"Age ")]/text()').extract_first()
                        if 'new' in age.lower():
                            self.item['age'] = '0'
                        if 'year' in age.lower():
                            self.item['age'] = re.findall('[0-9]+', age)[0] + 'year(s)'
                        elif 'month' in age.lower():
                            self.item['age'] = re.findall('[0-9]+', age)[0] + 'month(s)'
                        else:
                            self.item['age'] = re.findall('[0-9]+', age)[0]

                    except:
                        self.item['age'] = '0'
                    if not self.item['age']:
                        self.item['age'] = '0'
                self.item['scraped_time'] = dt.now().strftime('%m/%d/%Y %H:%M:%S')

                if (((not self.item['Monthly_Rent'] == '0') and (not self.item['Bua_sqft'] == '0') and (not self.item['Building_name'] == 'None') and (not self.item['lat'] == '0')) or (not self.item['Selling_price'] == '0') and (not self.item['Bua_sqft'] == '0') and (not self.item['Building_name'] == 'None') and (not self.item['lat'] == '0')) or ((not self.item['price_per_sqft'] == '0') and (not self.item['Bua_sqft'] == '0') and (not self.item['Building_name'] == 'None') and (not self.item['lat'] == '0')):
                    self.item['quality4'] = 1
                elif (((not self.item['price_per_sqft'] == '0') and (not self.item['Building_name'] == 'None') and (not self.item['lat'] == '0')) or ((not self.item['Selling_price'] == '0') and (not self.item['Bua_sqft'] == '0') and (not self.item['lat'] == '0')) or ((not self.item['Monthly_Rent'] == '0') and (not self.item['Bua_sqft'] == '0') and (not self.item['lat'] == '0')) or ((not self.item['Selling_price'] == '0') and (not self.item['Bua_sqft'] == '0') and (not self.item['Building_name'] == 'None')) or ((not self.item['Monthly_Rent'] == '0') and (not self.item['Bua_sqft'] == '0') and (not self.item['Building_name'] == 'None'))):
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

                price_check = 1

                yield self.item
            except Exception as e:
                print(e)

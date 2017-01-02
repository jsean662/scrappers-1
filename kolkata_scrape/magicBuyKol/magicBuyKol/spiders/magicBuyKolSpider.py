import scrapy
from magicBuyKol.items import MagicbuykolItem
from scrapy.selector import Selector
import datetime
from datetime import datetime as dt
import re


class MagicbuykolspiderSpider(scrapy.Spider):
    name = "magicBuyKolkata"
    allowed_domains = ["http://www.magicbricks.com/"]
    start_urls = ['http://www.magicbricks.com//']

    start_urls = [
        'http://www.magicbricks.com/property-for-sale/residential-real-estate?proptype=Multistorey-Apartment,Builder-Floor-Apartment,Penthouse,Studio-Apartment,Residential-House,Villa&cityName=Kolkata/Page-%s' % page for page in range(1, 1411)
    ]

    custom_settings = {
        'DEPTH_LIMIT': 10000,
        'DOWNLOAD_DELAY': 5}

    def parse(self, response):
        record = Selector(response)

        data = record.xpath('//div[contains(@id,"resultBlockWrapper")]')

        for i in data:
            item = MagicbuykolItem()

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
            item['monthly_rent'] = '0'
            item['price_per_sqft'] = '0'

            item['scraped_time'] = dt.now().strftime('%m/%d/%Y %H:%M:%S')

            item['city'] = 'Kolkata'

            item['Building_name'] = i.xpath('div/input[contains(@id,"projectName")]/@value').extract_first()
            if item['Building_name'] == '':
                item['Building_name'] = 'None'

            try:
                item['longt'] = i.xpath('div/div[@class="srpColm2"]/div[@class="proColmleft"]/div[@class="proNameWrap proNameWrapBuy"]/div[@class="proNameColm1"]/span[@class="seeOnMapLink seeOnMapLinkBuy"]/span[@class="stopParentLink"]/@onclick').extract_first().split('&')[0].split('?')[-1].split("=")[-1] # .xpath('.//input[@itemprop="latitude"]/@value').extract_first()
                if item['longt'] == '':
                    item['longt'] = '0'
            except:
                item['longt'] = '0'

            try:
                item['lat'] = i.xpath('div/div[@class="srpColm2"]/div[@class="proColmleft"]/div[@class="proNameWrap proNameWrapBuy"]/div[@class="proNameColm1"]/span[@class="seeOnMapLink seeOnMapLinkBuy"]/span[@class="stopParentLink"]/@onclick').extract_first().split('&')[1].split("=")[-1]
                if item['lat'] == '':
                    item['lat'] = '0'
            except:
                item['longt'] = '0'

            item['platform'] = 'magicbricks'
            item['carpet_area'] = '0'

            ids = i.xpath('@id').extract_first()
            item['data_id'] = re.findall('[0-9]+', ids)[0]

            item['config_type'] = i.xpath('.//input[contains(@id,"bedroomVal")]/@value').extract_first().replace('>', '')
            item['config_type'] = item['config_type']+'BHK'

            item['property_type'] = i.xpath('.//p[@class="proHeading"]/a/input[2]/@value').extract_first()
            if (item['property_type'] == 'Studio Apartment'):
                item['config_type'] = '1RK'

            ####### config_type is assumed as 'None' for default #########

            if item['config_type'] == 'BHK':
                item['config_type'] = 'None'
            
            try:
                sqf = i.xpath('.//input[contains(@id,"propertyArea")]/@value').extract_first()
                if 'sqft' in sqf:
                    item['Bua_sqft'] = re.findall('[0-9]+', sqf)
                elif 'kottah' in sqf:
                    item['Bua_sqft'] = re.findall('[0-9]+', sqf)
                    item['Bua_sqft'] = str(eval(item['Bua_sqft'][0]) * 720)
                else:
                    item['Bua_sqft'] = '0'
            except:             
                item['Bua_sqft'] = '0'

            item['Locality'] = i.xpath('div/div[@class="srpColm2"]/div[@class="proColmleft"]/div[1]/div/p/a/abbr/span[1]/span/text()').extract_first()

            try:
                stat = i.xpath('.//div[1]/div[2]/div[1]/div[2]/div[1]/text()').extract()
                if 'Under Construction' in stat:
                    item['Status'] = 'Under Construction'
                    poss = stat.split('Ready by ')[-1].replace("'", "").replace(')','').replace('\n', '').replace('. Freehold', '')
                    #print("POSSESSION: ", poss)
                    yr = str(re.findall('[0-9]+', poss))
                    yr = yr.replace('[', '').replace(']', '').replace('u', '').replace("'", "")
                    if 'Jan' in poss:
                        item['Possession'] = '01/01/' + yr + ' 00:00:00'
                    if 'Feb' in poss:
                        item['Possession'] = '01/02/' + yr + ' 00:00:00'
                    if 'Mar' in poss:
                        item['Possession'] = '01/03/' + yr + ' 00:00:00'
                    if 'Apr' in poss:
                        item['Possession'] = '01/04/' + yr + ' 00:00:00'
                    if 'May' in poss:
                        item['Possession'] = '01/05/' + yr + ' 00:00:00'
                    if 'Jun' in poss:
                        item['Possession'] = '01/06/' + yr + ' 00:00:00'
                    if 'Jul' in poss:
                        item['Possession'] = '01/07/' + yr + ' 00:00:00'
                    if 'Aug' in poss:
                        item['Possession'] = '01/08/' + yr + ' 00:00:00'
                    if 'Sep' in poss:
                        item['Possession'] = '01/09/' + yr + ' 00:00:00'
                    if 'Oct' in poss:
                        item['Possession'] = '01/10/' + yr + ' 00:00:00'
                    if 'Nov' in poss:
                        item['Possession'] = '01/11/' + yr + ' 00:00:00'
                    if 'Dec' in poss:
                        item['Possession'] = '01/12/' + yr + ' 00:00:00'                    
                else:
                    item['Status'] = 'Ready to move'
                    item['Possession'] = '0'
            except:
                item['Possession'] = '0'           

            price = i.xpath('.//div/div[@class="srpColm2"]/div[@class="proColmRight"]/div/div/div/span/text()').extract_first()
            if not price == None:
                if 'Lac' in price:
                    item['Selling_price'] = str(float(price.split()[0])*100000)
                elif 'Cr' in price:
                    item['Selling_price'] = str(float(price.split()[0])*10000000)
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
                sqft_per = i.xpath('div/div[@class="srpColm2"]/div[@class="proColmRight"]/div[@class="proPriceColm2"]/div[@class="proPriceColm2"]/div[@class="sqrPrice"]/span[@class="sqrPriceField"]/text()').extract_first()
                if sqft_per:
                    item['price_per_sqft'] = ''.join(re.findall('[0-9]+', sqft_per))
                else:
                    item['price_per_sqft'] = '0'
                if 'kottah' in sqf:
                    item['price_per_sqft'] = str(eval(item['price_per_sqft']) / 720)
            except:
                item['price_per_sqft'] = '0'

            try:
                item['name_lister'] = i.xpath('div/div[@class="srpColm2"]/div[@class="proColmleft"]/div[@class="proDetailsRow "]/input[contains(@id,"devName")]/@value').extract_first()
                if (item['name_lister'] == '') or (item['name_lister'] == 'null') :
                    item['name_lister'] = 'None'
            except:
                item['name_lister'] = 'None'

            item['txn_type'] = i.xpath('div/input[contains(@id,"transactionType")]/@value').extract_first()

            day = i.xpath('div/input[contains(@id,"createDate")]/@value').extract_first()

            item['listing_date'] = dt.strftime(dt.strptime(day, "%b %d, '%y"), '%m/%d/%Y %H:%M:%S')
            item['updated_date'] = item['listing_date']

            try:
                item['listing_by'] = i.xpath('.//div[@class="proAgentWrap"]/div[1]/div/div[1]/text()').extract_first()
                item['name_lister'] = i.xpath('.//div[@class="proAgentWrap"]/div[@class="comNameElip"]/text()').extract_first().replace("\n", "")
            except:
                item['listing_by'] = 'None'
                item['name_lister'] = 'None'

            if (((not item['Bua_sqft']=='0') and (not item['Building_name']=='None') and (not item['lat']=='0')) or ((not item['Selling_price'] == '0') and (not item['Bua_sqft']=='0') and (not item['Building_name']=='None') and (not item['lat']=='0')) or ((not item['price_per_sqft'] == '0') and (not item['Bua_sqft']=='0') and (not item['Building_name']=='None') and (not item['lat']=='0'))):
                item['quality4'] = 1
            elif (((not item['price_per_sqft'] == '0') and (not item['Building_name']=='None') and (not item['lat']=='0')) or ((not item['Selling_price'] == '0') and (not item['Bua_sqft']=='0') and (not item['lat']=='0')) or ((not item['Bua_sqft']=='0') and (not item['lat']=='0')) or ((not item['Selling_price'] == '0') and (not item['Bua_sqft']=='0') and (not item['Building_name']=='None')) or ((not item['Bua_sqft']=='0') and (not item['Building_name']=='None'))):
                item['quality4'] = 0.5
            else:
                item['quality4'] = 0
            if ((not item['Building_name'] == 'None') and (not item['listing_date'] == '0') and (not item['txn_type'] == 'None') and (not item['property_type'] == 'None') and ((not item['Selling_price'] == '0'))):
                item['quality1'] = 1
            else:
                item['quality1'] = 0

            if ((not item['Launch_date'] == '0') and (not item['Possession'] == '0')):
                item['quality2'] = 1
            else:
                item['quality2'] = 0

            if ((not item['mobile_lister'] == 'None') or (not item['listing_by'] == 'None') or (not item['name_lister'] == 'None')):
                item['quality3'] = 1
            else:
                item['quality3'] = 0
            yield item
        

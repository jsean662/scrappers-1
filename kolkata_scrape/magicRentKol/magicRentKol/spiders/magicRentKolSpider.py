import scrapy
from magicRentKol.items import MagicrentkolItem
from scrapy.spiders import Spider
from scrapy.spiders import CrawlSpider, Rule
from scrapy.selector import Selector
from scrapy.http import Request
from scrapy.http import FormRequest
# from urlparse import urljoin
from datetime import datetime as dt
from datetime import time, timedelta
from datetime import date
# import time
import re

class MagicrentkolspiderSpider(scrapy.Spider):
    name = "magicRentKolkata"
    allowed_domains = ['magicbricks.com']
    start_urls = (
        'http://www.magicbricks.com/property-for-rent/residential-real-estate?proptype=Multistorey-Apartment,Builder-Floor-Apartment,Penthouse,Studio-Apartment,Service-Apartment,Residential-House,Villa&cityName=Kolkata/Page-%s' % page for page in range(1, 453)
    )

    custom_settings = {
        'DEPTH_LIMIT': 1000,
        'DOWNLOAD_DELAY': 5,
    }

    def parse(self, response):
        # record = Selector(response)

        data = response.xpath('//div[@class="srpBlockListRow srpRentListRow"]') # response.xpath('//div[@class="srpBlockWrapper"]')record.xpath('//div[@class="srpColm2"]/div[@class="proColmleft"]')
        lister = response.xpath('//div[@class="srpColm2"]')
        dates = response.xpath('//span[@class="postedBy"]')
        k = 0
        for i in data:
            item = MagicrentkolItem()
            
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
            item['scraped_time'] = dt.now().strftime('%m/%d/%Y %H:%M:%S')

            item['platform'] = 'magicbrick'
            item['txn_type'] = 'Rent'

            item['property_type'] = i.xpath('.//p[@class="proHeading"]/a/input[2]/@value').extract_first()
            if item['property_type'] == 'Studio Apartment' or (item['property_type'] == 'Apartment'):
                item['config_type'] = '1RK'

            item['city'] = 'Kolkata'
            item['data_id'] = re.findall('[0-9]+', i.xpath('@id').extract_first())[0]

            #item['lat'] = i.xpath('.//div[@itemprop="geo"]/input[2]/@value').extract_first() 
            lat_longt = i.xpath('.//a[@class="Rent-SeeOnMapLink"]/@onclick').extract_first().split('?')[1]
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

            
            item['locality'] = i.xpath('.//div[@itemprop="address"]/input[@itemprop="addressLocality"]/@value').extract_first(default='None') # .xpath('div[1]/div[1]/div[1]/div[2]/p/a/span[1]/span/text()').extract_first()
            item['Building_name'] = i.xpath('.//input[contains(@id,"projectSocietyName")]/@value').extract_first() # .xpath('div[1]/div[1]/div[1]/div[2]/p/a/span[1]/text()').extract_first().replace("in","").replace("\n","")
            if item['Building_name'] == '':
                item['Building_name'] = 'None'
            
            item['config_type'] = i.xpath('.//input[contains(@id,"bedroomVal")]/@value').extract_first().replace('>', '')
            item['config_type'] = item['config_type']+'BHK'

            if item['property_type'] == 'Studio Apartment':
                item['config_type'] = '1RK'

            ###############  config_type assumed None for Apartments, House, Villa #################

            if item['config_type'] == 'BHK':
                item['config_type'] = 'None'

            item['Selling_price'] = '0'
            
            try:
                price = i.xpath('.//div[@class="proPrice"]/span[1]/text()').extract_first() 
            except:
                price = '0'

            if 'Lac' in price:
                price = float(price.replace("Lac", ""))*100000
                item['Monthly_Rent'] = str(price)
            elif 'Call for Price' in price:
                item['Monthly_Rent'] ='0'
            else:
                price = price.replace(",", "")
                item['Monthly_Rent'] = str(eval(price))
            
            if item['Selling_price'] == '0' and item['Monthly_Rent'] == '0':
                item['price_on_req'] = 'true'
            else:
                item['price_on_req'] = 'false'
            # item['carpet_area'] = 'None'

            try:
                list_by = i.xpath('.//div[@class="proAgentWrap"]/div[1]/div[1]/div[1]/text()').extract_first()
                if 'Agent' in list_by:
                    item['listing_by'] = 'Agent'
                elif 'Owner' in list_by:
                    item['listing_by'] = 'Owner'
                else:
                    item['listing_by'] = 'None'
            except:
                item['listing_by'] = 'None'

            item['name_lister'] = i.xpath('.//div[@class="comNameElip"]/text()').extract_first().replace('\n', ' ')
            if 'null' in item['name_lister']:
                item['name_lister'] = 'None'

            try:
                sqf = i.xpath('.//div[@class="proDetailsRow proDetailsRowListing proDetailsRowRent"]/div[1]/ul/li[1]/span/text()').extract_first()
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

            if 'Immediately' in status:
                item['Possession'] = 0
                item['Status'] = 'Ready To Move'
            else:
                if 'Available on' in status:
                    yr = re.findall('[0-9]+', status)
                    if 'Jan' in status:
                        item['Possession'] = '01/01/' + yr + '00:00:00'
                    if 'Feb' in status:
                        item['Possession'] = '01/02/' + yr + '00:00:00'
                    if 'Mar' in status:
                        item['Possession'] = '01/03/' + yr + '00:00:00'
                    if 'Apr' in status:
                        item['Possession'] = '01/04/' + yr + '00:00:00'
                    if 'May' in status:
                        item['Possession'] = '01/05/' + yr + '00:00:00'
                    if 'Jun' in status:
                        item['Possession'] = '01/06/' + yr + '00:00:00'
                    if 'Jul' in status:
                        item['Possession'] = '01/07/' + yr + '00:00:00'
                    if 'Aug' in status:
                        item['Possession'] = '01/08/' + yr + '00:00:00'
                    if 'Sep' in status:
                        item['Possession'] = '01/09/' + yr + '00:00:00'
                    if 'Oct' in status:
                        item['Possession'] = '01/10/' + yr + '00:00:00'
                    if 'Nov' in status:
                        item['Possession'] = '01/11/' + yr + '00:00:00'
                    if 'Dec' in status:
                        item['Possession'] = '01/12/' + yr + '00:00:00'
                item['Status'] = 'Under Construction'

            item['Details'] = i.xpath('.//input[@itemprop="description"]/@value').extract_first(default='None') # str(i.xpath('div[2]/div[1]/ul/li[2]/text()').extract_first())+' '+str(i.xpath('div[2]/div[1]/ul/li[3]/text()').extract_first())+' '+str(i.xpath('div[2]/div[1]/ul/li[4]/text()').extract_first())+' '+str(i.xpath('div[2]/div[1]/ul/li[5]/text()').extract_first())

            day = dates.xpath('text()').extract_first()
            day = day.replace("Posted: ", "").replace("Posted ", "")

            if 'Today' in day:
                item['listing_date'] = str(date.today().month)+'/'+str(date.today().day)+'/'+str(date.today().year)
            elif 'Yesterday' in day:
                item['listing_date'] = str((date.today() - timedelta(days=1)).month)+"/"+str((date.today() - timedelta(days=1)).day)+"/"+str((date.today() - timedelta(days=1)).year)
            elif 'th' in day:
                day = day.replace("th", "")
                day = dt.strftime(dt.strptime(day, '%d %b'), '%m/%d')+'/'+str(date.today().year)
                item['listing_date'] = day
            elif 'st' in day:
                day = day.replace("st", "")
                day = dt.strftime(dt.strptime(day, '%d %b'), '%m/%d')+'/'+str(date.today().year)
                item['listing_date'] = day
            elif 'rd' in day:
                day = day.replace("rd", "")
                day = dt.strftime(dt.strptime(day, '%d %b'), '%m/%d')+'/'+str(date.today().year)
                item['listing_date'] = day
            elif 'nd' in day:
                day = day.replace("nd", "")
                day = dt.strftime(dt.strptime(day, '%d %b'), '%m/%d')+'/'+str(date.today().year)
                item['listing_date'] = day
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



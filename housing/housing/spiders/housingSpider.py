import scrapy
from housing.items import HousingItem
from scrapy.spiders import Spider
from scrapy.spiders import CrawlSpider, Rule
from scrapy.selector import Selector
import json
from scrapy.http import Request
from datetime import datetime as dt
from datetime import time,timedelta
from datetime import date
import time

class HousingSpider(scrapy.Spider):
    name = 'housing'
    
    allowed_domains = ['housing.com']
    start_urls = ['https://housing.com/in/buy/mumbai/mumbai_1?page=1' ]#, 'https://housing.com/in/buy/mumbai/mmr?page=1']

    custom_settings = {
        'DEPTH_LIMIT' : 5000,
        'DOWNLOAD_DELAY' : 3
    }    
    
    def parse(self,response):
        hxs = Selector(response)
        pageNo = int(response.url.split('=')[-1])    
        
        #body1 = response.body
        #print body1
        #print pageNo,type(pageNo)
        data = hxs.xpath('//div[@class="list-card-item"]')
        #print data
        for i in data:
            item = HousingItem()
            webdata = i.xpath('div/@data-item-model').extract()
            jsondata = json.loads(webdata[0])
            #print item,jsondata
            room = jsondata['inventory_configs']
            count = len(room)
            #print count
            for j in range(0,count):

                item['data_id'] = jsondata['inventory_configs'][j]['flat_config_id']
                
                try:
                    item['mobile_lister'] = jsondata['contact_persons_info'][0]['contact_no']
                except:
                    item['mobile_lister'] = 'None'

                try:
                    item['name_lister'] = jsondata['contact_persons_info'][0]['name']
                except:
                    item['name_lister'] = 'None'

                try:
                    if ('Builtup Area' in jsondata['display_area_type']) or ('Saleable Area' in jsondata['display_area_type']):
                        item['Bua_sqft'] = jsondata['inventory_configs'][j]['area']
                        item['carpet_area'] = 0
                    if ('Carpet Area' in jsondata['display_area_type']):
                        item['carpet_area'] = jsondata['inventory_configs'][j]['area']
                        item['Bua_sqft'] = 0
                except KeyError:
                    item['Bua_sqft'] = jsondata['inventory_configs'][j]['area']

                item['management_by_landlord'] = 'None'

                item['areacode'] = 'None'

                item['google_place_id'] = 'None'

                item['Possession'] = time.strftime('%m/%d/%Y %H:%M:%S', time.gmtime(jsondata['completion_date']))

                try:
                    item['updated_date'] = str(time.strftime('%m/%d/%Y %H:%M:%S', time.gmtime(jsondata['updated_at'])))
                except:
                    item['updated_date'] = 'None'

                item['Launch_date'] = 'None'

                item['age'] = 'None'

                item['address'] = jsondata['street_info']

                item['price_on_req'] = jsondata['inventory_configs'][j]['price_on_request']

                item['sublocality'] = jsondata['polygons_hash']['sublocality']['name']

                item['config_type'] = str(jsondata['inventory_configs'][j]['number_of_bedrooms']) + 'BHK'

                item['platform'] = 'housing'

                item['city'] = jsondata['polygons_hash']['city']['name']

                dates = jsondata['date_added'].replace("T"," ").replace("Z","")
                item['listing_date'] = dt.strftime(dt.strptime(dates,"%Y-%m-%d %H:%M:%S"),"%m/%d/%Y %H:%M:%S")

                item['txn_type'] = jsondata['type']

                item['property_type'] = 'Residential'

                try:
                    item['Building_name'] = jsondata['name']
                except:
                    item['Building_name'] = 'None'

                item['lat'] = jsondata['location_coordinates'].split(",")[0]

                item['longt'] = jsondata['location_coordinates'].split(",")[-1]

                item['locality'] = jsondata['polygons_hash']['locality']['name']

                item['price_per_sqft'] = jsondata['inventory_configs'][j]['per_sqft_rate']

                item['Status'] = 'None'

                item['listing_by'] = 'None'

                item['Selling_price'] = str(jsondata['inventory_configs'][j]['price'])

                item['Monthly_Rent'] = '0'

                item['Details'] = 'None'

                if ((not item['Building_name'] == 'None') and (not item['listing_date'] == 'None') and (not item['txn_type'] == 'None') and (not item['property_type'] == 'None') and ((not item['Selling_price'] == '0') or (not item['Monthly_Rent'] == '0'))):
                    item['quality1'] = 1
                else:
                    item['quality1'] = 0

                if ((not item['Launch_date'] == 'None') and (not item['Possession'] == 'None')):
                    item['quality2'] = 1
                else:
                    item['quality2'] = 0

                if ((not item['mobile_lister'] == 'None') or (not item['listing_by'] == 'None') or (not item['name_lister'] == 'None')):
                    item['quality3'] = 1
                else:
                    item['quality3'] = 0
                yield item

        
        next_url = response.url.split("=")[0] + '=' + str(pageNo+1)
        yield Request(next_url,callback=self.parse)


    '''    jsnr = response.body
        jsndata = json.loads(jsnr)
        
        curValue = int(response.url.split('&')[-1].split('=')[-1])
        
        path = jsndata['hits']
        total = jsndata['total']
        last = jsndata['is_last_page']
        
        if last :
            no = 20-((curValue*20)-total)
        else:
            no = 20
        #print total
        for i in range(0,no):
            
            item = HousingItem()
            
            item['platform'] = 'housing'
            #price = path[i]['price']
            #if not str(price) == '':
            #    item['Selling_price'] = str(price)
            #else:
            #    item['Selling_price'] = '0'
            item['Selling_price'] = str(path[i]['price'])
            if item['Selling_price'] == 'None':
                item['Selling_price'] = '0'
            item['Monthly_Rent'] = '0'
            item['lat'] = path[i]['location_coordinates'].split(',')[0]
            item['longt'] = path[i]['location_coordinates'].split(',')[-1]
            item['city'] = path[i]['polygons_hash']['city']['name']
            item['locality'] = path[i]['polygons_hash']['locality']['name']
            item['sublocality'] = path[i]['polygons_hash']['sublocality']['name']
            item['data_id'] = path[i]['id']
            dates = path[i]['date_added'].replace("T"," ").replace("Z","")
            item['listing_date'] = dt.strftime(dt.strptime(dates,"%Y-%m-%d %H:%M:%S"),"%m/%d/%Y %H:%M:%S")
            item['address'] = path[i]['street_info']
            item['config_type'] = path[i]['title'].replace("Apartment","").replace("Apartments","").replace("Independent Floor","").replace(" Independent House","").replace(" Duplexes","")
            item['txn_type'] = path[i]['type']
            item['price_on_req'] = path[i]['inventory_configs'][0]['price_on_request']
            item['property_type'] = 'Residential'
            item['sqft'] = path[i]['inventory_configs'][0]['area']
            item['Status'] = 'None'
            item['Building_name'] = 'None'
            item['listing_by'] = 'None'
            item['name_lister'] = 'None'
            item['Details'] = 'None'
            item['age'] = 'None'
            item['google_place_id'] = 'None'
            item['immediate_possession'] = 'None'
            item['mobile_lister'] = 'None'
            item['areacode'] = 'None'
            item['management_by_landlord'] = 'None'
            item['carpet_area'] = 'None'
            item['updated_date'] = item['listing_date']
                  
            yield item
        
        
        if not last :
            next_url = 'https://buy.housing.com/api/v1/buy/index/filter?placeholder_ids=6,2,3,7&sort_key=relevance&poly=63913984110fb4e5c0b4&results_per_page=20&show_collections=true&show_aggregations=true&np_total_count=80&resale_total_count=1635&np_offset=0&resale_offset=-2&p=' + str(curValue+1)
            yield Request(next_url,self.parse)'''
            
              
            

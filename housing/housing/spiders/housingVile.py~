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
    name = 'housingVile'
    
    allowed_domains = ['housing.com']
    start_urls = ['https://buy.housing.com/api/v1/buy/index/filter?placeholder_ids=6,2,3,7&sort_key=relevance&poly=7c9bf8c4bf259dbf3733&results_per_page=20&show_collections=true&show_aggregations=true&source=seo&p=1']

    custom_settings = {
        'DEPTH_LIMIT' : 1000,
        'DOWNLOAD_DELAY' : 3
    }    
    
    def parse(self,response):
        #hxs = Selector(response)
        
        jsnr = response.body
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
            item['address'] = path[i]['street_info']
            dates = path[i]['date_added'].replace("T"," ").replace("Z","")
            item['listing_date'] = dt.strftime(dt.strptime(dates,"%Y-%m-%d %H:%M:%S"),"%m/%d/%Y %H:%M:%S")
            item['config_type'] = path[i]['title'].replace("Apartment","").replace("Apartments","").replace("Independent Floor","").replace(" Independent House","").replace(" Duplexes","")
            item['txn_type'] = path[i]['type']
            item['price_on_req'] = path[i]['inventory_configs'][0]['price_on_request']
            item['property_type'] = 'Residential'
            item['sqft'] = path[i]['inventory_configs'][0]['area']
            item['Building_name'] = 'None'
            item['listing_by'] = 'None'
            item['age'] = 'None'
            item['name_lister'] = 'None'
            item['Details'] = 'None'
            item['google_place_id'] = 'None'
            item['immediate_possession'] = 'None'
            item['mobile_lister'] = 'None'
            item['areacode'] = 'None'
            item['management_by_landlord'] = 'None'
                        
            yield item
        
        
        if not last :
            next_url = 'https://buy.housing.com/api/v1/buy/index/filter?placeholder_ids=6,2,3,7&sort_key=relevance&poly=7c9bf8c4bf259dbf3733&results_per_page=20&show_collections=true&show_aggregations=true&source=seo&p=' + str(curValue+1)
            yield Request(next_url,self.parse)
            
              
            

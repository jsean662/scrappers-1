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
    start_urls = ['https://buy.housing.com//api/v3/buy/index/filter?source=web&poly=32964110855b9736fd94&p=1&sort_key=date_added&show_collections=true&show_aggregations=true&placeholder_ids=6,2,3,7&p=1']
    #https://buy.housing.com//api/v3/buy/index/filter?source=web&poly=1ca99c33e3d8b987ccf1&sort_key=date_added&show_collections=true&show_aggregations=true&placeholder_ids=6,2,3,7&p=1

    custom_settings = {
        'DEPTH_LIMIT' : 5000,
        'DOWNLOAD_DELAY' : 3
    }    
    
    def parse(self,response):
        data  = json.loads(response.body)
        pageNo = int(response.url.split('=')[-1])
        path = data['hits']

        no = len(path)

        for i in range(0,no):
            item = HousingItem()

            count = len(path[i]['inventory_configs'])

            for j in range(0,count):
                item['data_id'] = path[i]['inventory_configs'][j]['id']

                item['txn_type'] = path[i]['type']

                item['property_type'] = 'Residential'

                dates = path[i]['date_added'].replace('T',' ').replace('Z','')
                item['listing_date'] = dt.strftime(dt.strptime(dates,'%Y-%m-%d %H:%M:%S'),'%m/%d/%Y %H:%M:%S')

                loc = path[i]['location_coordinates']
                item['lat'] = loc.split(',')[0]
                item['longt'] = loc.split(',')[-1]

                item['Selling_price'] = path[i]['inventory_configs'][j]['price']

                item['Monthly_Rent'] = '0'

                item['Bua_sqft'] = path[i]['inventory_configs'][j]['area']

                item['config_type'] = str(path[i]['inventory_configs'][j]['number_of_bedrooms']) + ' BHK'

                pos = path[i]['inventory_configs'][j]['completion_date']
                item['Possession'] = time.strftime('%m/%d/%Y %H:%M:%S',time.gmtime(pos))

                item['price_per_sqft'] = path[i]['inventory_configs'][j]['per_sqft_rate']

                item['price_on_req'] = path[i]['inventory_configs'][j]['price_on_request']

                try:
                    item['name_lister'] = path[i]['contact_persons_info'][0]['name']
                except:
                    item['name_lister'] = 'None'

                item['city'] = 'mumbai'

                try:
                    item['updated_date'] = time.strftime('%m/%d/%Y %H:%M:%S',time.gmtime(path[i]['updated_at']))
                except:
                    item['updated_date'] = item['listing_date']

                try:
                    item['locality'] = path[i]['display_neighbourhood'][1]
                except:
                    item['locality'] = 'None'

                '''
                Assignning Default values
                '''
                item['carpet_area'] = '0'
                item['management_by_landlord'] = 'None'
                item['areacode'] = 'None'
                item['mobile_lister'] = 'None'
                item['google_place_id'] = 'None'
                item['Launch_date'] = 'None'
                item['age'] = 'None'
                item['address'] = 'None'
                item['sublocality'] = 'None'
                item['platform'] = 'housing'
                item['Building_name'] = 'None'
                item['Status'] = 'None'
                item['listing_by'] = 'None'
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

        if data['is_last_page']==False:
            next_url = 'https://buy.housing.com//api/v3/buy/index/filter?source=web&poly=32964110855b9736fd94&p=1&sort_key=date_added&show_collections=true&show_aggregations=true&placeholder_ids=6,2,3,7&p='+str(pageNo+1)
            yield Request(next_url,callback=self.parse)

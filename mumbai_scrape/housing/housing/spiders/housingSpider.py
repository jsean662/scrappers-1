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
    name = 'housingMumbai'
    
    allowed_domains = ['housing.com']
    start_urls = ['https://buy.housing.com//api/v3/buy/index/filter?source=web&poly=1ca99c33e3d8b987ccf1&sort_key=date_added&total=27998&np_total_count=1888&resale_total_count=26110&np_offset=0&resale_offset=0&is_last_page=false&project_flat_config_count=5244&negative_aggregation={}&show_collections=true&show_aggregations=true&placeholder_ids=2,3,6,7&p=1']

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

                try:
                    item['Building_name'] = path[i]['name']
                except:
                    item['Building_name'] = 'None'

                item['property_type'] = 'Residential'

                dates = path[i]['date_added'].replace('T',' ').replace('Z','')
                item['listing_date'] = dt.strftime(dt.strptime(dates,'%Y-%m-%d %H:%M:%S'),'%m/%d/%Y %H:%M:%S')

                loc = path[i]['location_coordinates']
                item['lat'] = loc.split(',')[0]
                item['longt'] = loc.split(',')[-1]

                item['Selling_price'] = path[i]['inventory_configs'][j]['price']

                item['Monthly_Rent'] = '0'

                item['Bua_sqft'] = path[i]['inventory_configs'][j]['area']

                item['config_type'] = str(path[i]['inventory_configs'][j]['number_of_bedrooms']) + 'BHK'

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

                item['scraped_time'] = dt.now().strftime('%m/%d/%Y %H:%M:%S')

                '''
                Assignning Default values
                '''
                item['carpet_area'] = '0'
                item['management_by_landlord'] = 'None'
                item['areacode'] = 'None'
                item['mobile_lister'] = 'None'
                item['google_place_id'] = 'None'
                item['Launch_date'] = '0'
                item['age'] = 'None'
                item['address'] = 'None'
                item['sublocality'] = 'None'
                item['platform'] = 'housing'
                item['Status'] = 'None'
                item['listing_by'] = 'None'
                item['Details'] = 'None'

                if (((not item['Monthly_Rent'] == '0') and (not item['Bua_sqft']=='0') and (not item['Building_name']=='None') and (not item['lat']=='0')) or ((not item['Selling_price'] == '0') and (not item['Bua_sqft']=='0') and (not item['Building_name']=='None') and (not item['lat']=='0')) or ((not item['price_per_sqft'] == '0') and (not item['Bua_sqft']=='0') and (not item['Building_name']=='None') and (not item['lat']=='0'))):
                    item['quality4'] = 1
                elif (((not item['price_per_sqft'] == '0') and (not item['Building_name']=='None') and (not item['lat']=='0')) or ((not item['Selling_price'] == '0') and (not item['Bua_sqft']=='0') and (not item['lat']=='0')) or ((not item['Monthly_Rent'] == '0') and (not item['Bua_sqft']=='0') and (not item['lat']=='0')) or ((not item['Selling_price'] == '0') and (not item['Bua_sqft']=='0') and (not item['Building_name']=='None')) or ((not item['Monthly_Rent'] == '0') and (not item['Bua_sqft']=='0') and (not item['Building_name']=='None'))):
                    item['quality4'] = 0.5
                else:
                    item['quality4'] = 0
                if ((not item['Building_name'] == 'None') and (not item['listing_date'] == '0') and (not item['txn_type'] == 'None') and (not item['property_type'] == 'None') and ((not item['Selling_price'] == '0') or (not item['Monthly_Rent'] == '0'))):
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

        if data['is_last_page']==False:
            next_url = 'https://buy.housing.com//api/v3/buy/index/filter?source=web&poly=1ca99c33e3d8b987ccf1&sort_key=date_added&total=27998&np_total_count=1888&resale_total_count=26110&np_offset=0&resale_offset=0&is_last_page=false&project_flat_config_count=5244&negative_aggregation={}&show_collections=true&show_aggregations=true&placeholder_ids=2,3,6,7&p='+str(pageNo+1)
            yield Request(next_url,callback=self.parse)

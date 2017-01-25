# -*- coding: utf-8 -*-
import scrapy
import json
from datetime import datetime as dt
from datetime import time, timedelta
import time
from ..items import HousingDelhiItem


class HousingdelhiSpider(scrapy.Spider):
    name = "housingDelhi"
    allowed_domains = ["housing.com"]
    start_urls = (
        'https://buy.housing.com//api/v3/buy/index/filter?source=web&poly=11e12081aa78a3375087&sort_key=date_added&np_offset=0&negative_aggregation={}&show_collections=true&p=%s' % page for page in range(1, 5072)
    )
    custom_settings = {
        'DEPTH_LIMIT': 5000,
        'DOWNLOAD_DELAY': 3,
    }

    def parse(self, response):
        data1 = (response.body).decode("utf-8")
        data = json.loads(data1)
        # pageNo = int(response.url.split('=')[-1])
        path = data['hits']

        no = len(path)

        for i in range(0, no):
            item = HousingDelhiItem()

            count = len(path[i]['inventory_configs'])

            for j in range(0, count):
                item['data_id'] = path[i]['inventory_configs'][j]['id']

                item['txn_type'] = path[i]['type']

                if 'project' in item['txn_type']:
                    item['listing_by'] = 'Builder'
                else:
                    try:
                        lister = path[i]['contact_persons_info'][0]['chat_enabled']
                        if lister is None or lister is False:
                            item['listing_by'] = 'None'
                        else:
                            if 'true' in lister:
                                item['listing_by'] = 'Agent'
                            elif 'false' in lister:
                                item['listing_by'] = 'Owner'
                    except:
                        item['listing_by'] = 'None'

                try:
                    item['Building_name'] = path[i]['building_name']
                except:
                    item['Building_name'] = 'None'

                item['property_type'] = 'Residential'

                dates = path[i]['date_added'].replace('T', ' ').replace('Z', '')
                item['listing_date'] = dt.strftime(dt.strptime(dates, '%Y-%m-%d %H:%M:%S'), '%m/%d/%Y %H:%M:%S')

                loc = path[i]['location_coordinates']
                item['lat'] = loc.split(',')[0]
                item['longt'] = loc.split(',')[1]

                try:
                    item['Selling_price'] = path[i]['inventory_configs'][j]['price']
                    if item['Selling_price'] is None:
                        item['Selling_price'] = 0
                except:
                    item['Selling_price'] = 0

                item['Monthly_Rent'] = '0'

                item['Bua_sqft'] = path[i]['inventory_configs'][j]['area']

                item['config_type'] = str(path[i]['inventory_configs'][j]['number_of_bedrooms']) + 'BHK'

                try:
                    pos = path[i]['inventory_configs'][j]['completion_date']
                    item['Possession'] = time.strftime('%m/%d/%Y %H:%M:%S', time.gmtime(pos))
                except:
                    print('')

                try:
                    item['price_per_sqft'] = path[i]['inventory_configs'][j]['per_sqft_rate']
                except:
                    item['price_per_sqft'] = 0

                item['price_on_req'] = path[i]['inventory_configs'][j]['price_on_request']

                try:
                    item['name_lister'] = path[i]['contact_persons_info'][0]['name']
                except:
                    item['name_lister'] = 'None'

                # try:
                #   item['city'] = path[i]['polygons_hash']['city']['name']
                # except:
                item['city'] = 'Delhi'

                item['sublocality'] = path[i]['polygons_hash']['sublocality']['name']
                if item['sublocality'] is None:
                    item['sublocality'] = 'None'

                try:
                    item['updated_date'] = time.strftime('%m/%d/%Y %H:%M:%S', time.gmtime(path[i]['updated_at']))
                except:
                    item['updated_date'] = item['listing_date']

                try:
                    item['locality'] = path[i]['display_neighbourhood'][1]
                except:
                    item['locality'] = 'None'

                item['scraped_time'] = dt.now().strftime('%m/%d/%Y %H:%M:%S')

                item['carpet_area'] = '0'
                item['management_by_landlord'] = 'None'
                item['areacode'] = 'None'
                item['mobile_lister'] = 'None'
                item['google_place_id'] = 'None'
                item['Launch_date'] = '0'
                item['age'] = '0'
                item['address'] = 'None'
                item['platform'] = 'Housing'

                try:
                    stat = path[i]['is_uc_property']
                    if stat is None:
                        item['Status'] = 'None'
                    else:
                        if 'false' in stat.lower():
                            item['Status'] = 'Ready To Move'
                        else:
                            item['Status'] = 'Under Construction'
                except:
                    if 'resale' in item['txn_type'].lower():
                        item['Status'] = 'Ready To Move'
                    else:
                        item['Status'] = 'Under Construction'

                item['Details'] = 'None'

                try:
                    if str(item['Building_name']).isdigit():
                        item['Building_name'] = 'None'

                    if len(item['Building_name']) < 3 or len(item['Building_name']) > 35:
                        item['Building_name'] = 'None'
                except:
                    pass

                if (((not item['Bua_sqft'] == '0') and (not item['Building_name'] == 'None') and (not item['lat'] == '0')) or ((not item['Selling_price'] == '0') and (not item['Bua_sqft'] == '0') and (not item['Building_name'] == 'None') and (not item['lat'] == '0')) or ((not item['price_per_sqft'] == '0') and (not item['Bua_sqft'] == '0') and (not item['Building_name'] == 'None') and (not item['lat'] == '0'))):
                    item['quality4'] = 1
                elif (((not item['price_per_sqft'] == '0') and (not item['Building_name'] == 'None') and (not item['lat'] == '0')) or ((not item['Selling_price'] == '0') and (not item['Bua_sqft'] == '0') and (not item['lat'] == '0')) or ((not item['Bua_sqft'] == '0') and (not item['lat'] == '0')) or ((not item['Selling_price'] == '0') and (not item['Bua_sqft'] == '0') and (not item['Building_name'] == 'None')) or ((not item['Bua_sqft'] == '0') and (not item['Building_name'] == 'None'))):
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

        '''if data['is_last_page']==False:
            next_url = 'https://buy.housing.com//api/v3/buy/index/filter?source=web&poly=eec306948307d1a640ac&sort_key=date_added&total=27998&np_total_count=1888&resale_total_count=26110&np_offset=0&resale_offset=0&is_last_page=false&project_flat_config_count=5244&negative_aggregation={}&show_collections=true&show_aggregations=true&placeholder_ids=2,3,6,7&p='+str(pageNo+1)
            yield Request(next_url, callback=self.parse)'''


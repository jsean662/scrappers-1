import scrapy
from acres.items import AcresItem
from scrapy.spiders import Spider
from scrapy.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.http import Request
from scrapy.selector import Selector
from scrapy.selector import HtmlXPathSelector
from urlparse import urljoin
import time
import datetime
from datetime import datetime as dt

class JagahaSpider(CrawlSpider):
    name = "aspy"
    allowed_domains = ['99acres.com']

    start_urls = [
            'http://www.99acres.com/property-in-mumbai-ffid-page-196?orig_property_type=R&class=O,A,B&search_type=QS&search_location=CP12&lstacn=SEARCH&pageid=QS&search_id=7019357638975910&src=PAGING&lastAcn=SEARCH&lastAcnId=7019357638975910',
            'http://www.99acres.com/rent-property-in-mumbai-ffid-page-1?orig_property_type=R&class=O,A,B&search_type=QS&search_location=CP12&pageid=QS&search_id=7024716630429298&src=PAGING&lastAcn=SEARCH&lastAcnId=7024716630429298&fsl_results=Y&total_fsl_count=2',
            'http://www.99acres.com/commercial-property-in-mumbai-ffid-page-1?orig_property_type=C&class=O,A,B&search_type=QS&search_location=SH&lstacn=SEARCH&pageid=QS&search_id=7025026338708533&src=PAGING&lastAcn=SEARCH&lastAcnId=7025026338708533&fsl_results=Y&total_fsl_count=2',
            'http://www.99acres.com/rent-commercial-property-in-mumbai-ffid-page-1?orig_property_type=C&class=O,A,B&search_type=QS&search_location=SH&lstacn=SEARCH&pageid=QS&keyword_orig=mumbai&search_id=7025187469574654&src=PAGING&lastAcn=SEARCH&lastAcnId=7025187469574654&fsl_results=Y&total_fsl_count='
            ]
    custom_settings = {
            'BOT_NAME': 'acres',
            'DEPTH_LIMIT': 1000,
            'DOWNLOAD_DELAY': 0
        }
    data_list = []
    def parse(self,response):
        hxs = Selector(response)
        path1 = "//div[@id='ysf']/h1"
        x1 = hxs.xpath(path1)
        path = "//div[@id='results']/div[1]/div[contains(@class,'srpWrap')]"
        x = hxs.xpath(path)
        
        for i in x:
            data_id = i.xpath("@data-propid").extract_first()
            if data_id not in self.data_list:
                try:
                    item = AcresItem()
                    self.data_list.append(data_id)
                    sqft_check = i.xpath("div[@class='srpDetail']/div[@class='srpDataWrap']/span[1]/b[1]/text()").extract_first().replace("Sq.Ft.","").replace("Sq. Meter","")
                    check = 0
                    #print sqft_check
                    if 'to' in sqft_check:
                        sqft1 = str(sqft_check.split('to')[0]).strip()
                        sqft2 = str(sqft_check.split('to')[1]).strip()
                        print sqft1,sqft2
                        sqft_list = [sqft1,sqft2]
                        print sqft_list
                    else:
                        sqft_list = [sqft_check]
                        print sqft_list
                    for s in sqft_list:
                        check = check + 1    
                        item['data_id'] = data_id
                        item['platform'] = '99acres'
                        item['property_type'] = x1.xpath("span[@id='ysfPropertyType']/b/text()").extract_first().split(" ")[1]
                        item['txn_type'] = x1.xpath("span[2]/b/text()").extract_first()
                        item['city'] = x1.xpath("span[3]/b/text()").extract_first().split(" ")[0]
                    
                        item['sqft'] =  s
                    
                        item['Building_name'] = str(i.xpath("div[@class='srpDetail']/div[@class='srpDataWrap']/span[2]/a/b/text()").extract_first())
                        if item['Building_name'] == '':
                            item['Building_name'] = 'None'
                    
                        item['Status'] = str(i.xpath("div[@class='srpDetail']/div[@class='srpDataWrap']/span[3]/span/text()").extract()).replace('\\xa0','').replace('u','').replace(',','').replace("'","")
                        if item['property_type'] == 'Residential':
                            item['config_type'] = i.xpath("div[@class='wrapttl']/div[1]/a/text()").extract_first().split(',')[0].replace("Sq.Ft.","").replace("(","").replace(")","")[:5]
                            if 'Bed' in item['config_type']:
                                item['config_type']  = item['config_type'].split(" ")[0] + ' BHK'
                            if not 'K' in item['config_type']:
                                item['config_type'] = 'None'
                        else:
                            item['config_type'] = 'None'
                        item['locality'] = i.xpath("div[@class='wrapttl']/div[1]/a/text()").extract_first().split(' in ')[-1]
                        date_string = str(i.xpath("div[@class='srpDetail']/div[last()]/text()").extract()).split(':')[-1].replace(' ','').replace(']','').replace('\\n','').replace("'","")
                        if date_string == 'Today':
                            date = time.strftime('%b%d,%Y')
                        else:
                            if date_string == 'Yesterday':
                                date = dt.strftime(dt.now()-datetime.timedelta(1),'%b%d,%Y')
                            else:
                                date = date_string
                        date = dt.strftime(dt.strptime(date,'%b%d,%Y'),'%m/%d/%Y %H:%M:%S')
                        item['listing_date'] = date
                        price = i.xpath("div[@class='wrapttl']/div[1]/b[2]/text()").extract_first()
                        if price:
                            if 'to' in price:
                                price1 = price.split('to')[0]
                                price2 = price.split('to')[1]
                            
                                if 'Lac' in price1:
                                    price1 = float(str(price1.split()[0])) * 100000
                                else:
                                    if 'Crore' in price1:
                                        price1 =  float(str(price1.split()[0])) * 10000000
                                if 'Lac' in price2:
                                    price2 = float(str(price2.split()[0])) * 100000
                                else:
                                    if 'Crore' in price2:
                                        price2 =  float(str(price2.split()[0])) * 10000000 
                                print price1 , price2
                                if check == 1:
                                    price = str(price1)
                                else:
                                    price = str(price2)
                            else:
                                if 'Lac' in price:
                                    price = [str(float(str(price.split()[0])) * 100000)]
                                else:
                                    if 'Crore' in price:
                                        price =  [str(float(str(price.split()[0])) * 10000000)]
                            if item['txn_type'] in 'On Rent':
                                item['Monthly_Rent'] = price
                                item['Selling_price'] = '0'
                            else:
                                item['Selling_price'] = price
                                item['Monthly_Rent'] = '0'
                        else:
                            if item['txn_type'] in 'On Rent':
                                item['Monthly_Rent'] = '0'
                                item['Selling_price'] = '0'
                            else:
                                item['Selling_price'] = '0'
                                item['Monthly_Rent'] = '0'
                        if item['Monthly_Rent'] == '0' and item['Selling_price'] == '0':
                            item['price_on_req'] = 'true'
                        else:
                            item['price_on_req'] = 'false'
                        lat_lng = str(i.xpath("div[@class='wrapttl']/i/@data-maplatlngzm").extract_first()).split(',')
                        item['lat'] = lat_lng[0]
                        if len(lat_lng)>1:
                            item['longt'] = lat_lng[1]
                        else:
                            item['longt'] = 'None'
                        item['listing_by'] = 'None'
                        item['name_lister'] = 'None'
                        item['Details'] = 'None'
                        item['address'] = 'None'
                        item['sublocality'] = 'None'
                        item['age'] = 'None'
                        item['google_place_id'] = 'None'
                        item['immediate_possession'] = 'None'
                        item['mobile_lister'] = 'None'
                        item['areacode'] = 'None'
                        item['management_by_landlord'] = 'None'
                        item['carpet_area'] = 'None'
                        item['updated_date'] = item['listing_date']
                        yield item
                except Exception:
                        print Exception
        
            page_path = "//div[@id='results']/div[1]/div[contains(@class,'pgdiv')]"
            page = hxs.xpath(page_path)
            page1 = page.xpath("span[@class='pgdis']/a[last()]/@href").extract_first()
            page2 = page.xpath("a[last()]/@href").extract_first()
            if page1:
                url = page1
                next_url = urljoin('http://www.99acres.com',url)
                yield Request(next_url, callback=self.parse)
            if page2:
                url = page2
                next_url = urljoin('http://www.99acres.com',url)
                yield Request(next_url, callback=self.parse)

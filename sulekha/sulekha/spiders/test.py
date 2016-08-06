from scrapy.spiders import BaseSpider
from scrapy.http import FormRequest
from scrapy.selector import Selector
from sulekha.items import PropertyItem
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors.sgml import SgmlLinkExtractor
from datetime import datetime as dt
import datetime
import time

class MySpider(CrawlSpider):
    name = "SulekhaSpider"
    allowed_domains = ['property.sulekha.com']
    start_urls = ["http://property.sulekha.com/property-in-mumbai-for-sale_page-1"]
    custom_settings = {
            'DEPTH_LIMIT': 7000,
            'DOWNLOAD_DELAY': 5
        }
    
    
    def parse(self, response):
        hxs = Selector(response)
        
        data = hxs.xpath("//li[@class='list-box']")
        
        for i in data:
            item = PropertyItem()

            item['data_id'] = i.xpath('div[@class="content"]/div[@class="action-info"]/div[@class="actions ad-contact"]/div[@class="ContactAdvDiv"]/div/@id').extract_first().replace('CB','')
            
            item['city'] = 'mumbai'
            item['platform'] = 'Sulekha'

            bldg = i.xpath('div[@class="header"]/div[@class="title"]/strong/a/@title').extract_first()
            if ((' at ' in bldg) and (' in ' in bldg)):
                item['Building_name'] = bldg.split(' in ')[-1].split(' at ')[0]
            else:
                item['Building_name'] = 'None'

            price = i.xpath('div[@class="header"]/div[@class="title"]/div[@class="price"]/text()').extract()[-1].strip()
            if 'lakhs' in price:
                price = str(float(price.split(" ")[0])*100000)
            elif 'crores' in price:
                price = str(float(price.split(" ")[0])*10000000)
            else:
                price = '0'
            item['Selling_price'] = price

            item['locality'] = i.xpath('div[@class="header"]/div[@class="title"]/p[@itemprop="address"]/a[@class="GAPListingLocation"]/span[@itemprop="addressLocality"]/text()').extract_first().split(',')[0].strip()

            item['lat'] = i.xpath('@data-lattitude').extract_first()

            item['longt'] = i.xpath('@data-longitude').extract_first()

            item['carpet_area'] = 'None'
            item['management_by_landlord'] = 'None'
            item['areacode'] = 'None'
            item['mobile_lister'] = 'None'
            item['google_place_id'] = 'None'
            item['Launch_date'] = 'None'
            item['Possession'] = 'None'
            item['config_type'] = 'None'
            item['Bua_sqft'] = 'None'
            item['property_type'] = 'None'
            item['txn_type'] = 'None'
            item['age'] = 'None'
            item['address'] = 'None'
            item['price_on_req'] = 'None'
            item['sublocality'] = 'None'
            item['price_per_sqft'] = 'None'
            item['name_lister'] = 'None'
            item['Monthly_Rent'] = 0

            try:
                li1 = i.xpath('div[@class="content"]/div[@class="seven columns"]/ul[@class="info"]/li[2]/span/text()').extract_first()
                li2 = i.xpath('div[@class="content"]/div[@class="seven columns"]/ul[@class="info"]/li[3]/span/text()').extract_first()
                li3 = i.xpath('div[@class="content"]/div[@class="seven columns"]/ul[@class="info"]/li[4]/span/text()').extract_first()
                li4 = i.xpath('div[@class="content"]/div[@class="seven columns"]/ul[@class="info"]/li[5]/span/text()').extract_first()
            except:
                print 'less data'
            
            if 'Bedrooms:' in li1:
                item['config_type'] = i.xpath('div[@class="content"]/div[@class="seven columns"]/ul[@class="info"]/li[2]/text()').extract_first()
            if 'Possession:' in li1:
                dates = i.xpath('div[@class="content"]/div[@class="seven columns"]/ul[@class="info"]/li[@itemprop="startDate"]/@content').extract_first()
                if dates == '':
                    item['Possession'] = i.xpath('div[@class="content"]/div[@class="seven columns"]/ul[@class="info"]/li[@itemprop="startDate"]/b/text()').extract_first()
                else:    
                    dates = dates.replace('T',' ')
                    item['Possession'] = dt.strftime(dt.strptime(dates,'%Y-%m-%d %H:%M:%S'),'%m/%d/%Y %H:%M:%S')
            if 'Area:' in li1:
                item['Bua_sqft'] = i.xpath('div[@class="content"]/div[@class="seven columns"]/ul[@class="info"]/li[2]/text()').extract_first()
            if 'Property Age:' in li1:
                item['age'] = i.xpath('div[@class="content"]/div[@class="seven columns"]/ul[@class="info"]/li[2]/text()').extract_first()

            if 'Possession:' in li2:
                dates = i.xpath('div[@class="content"]/div[@class="seven columns"]/ul[@class="info"]/li[@itemprop="startDate"]/@content').extract_first()
                if dates == '':
                    item['Possession'] = i.xpath('div[@class="content"]/div[@class="seven columns"]/ul[@class="info"]/li[@itemprop="startDate"]/b/text()').extract_first()
                else:
                    dates = dates.replace('T',' ')
                    item['Possession'] = dt.strftime(dt.strptime(dates,'%Y-%m-%d %H:%M:%S'),'%m/%d/%Y %H:%M:%S')
            if 'Builtup-Area:' in li2:
                item['Bua_sqft'] = i.xpath('div[@class="content"]/div[@class="seven columns"]/ul[@class="info"]/li[3]/text()').extract_first().split(' ')[0]
            if 'Sub Type:' in li2:
                item['property_type'] = i.xpath('div[@class="content"]/div[@class="seven columns"]/ul[@class="info"]/li[3]/text()').extract_first().split(' ')[0]
            if 'Property Age:' in li2:
                item['age'] = i.xpath('div[@class="content"]/div[@class="seven columns"]/ul[@class="info"]/li[3]/text()').extract_first()

            if 'Builtup-Area:' in li3:
                item['Bua_sqft'] = i.xpath('div[@class="content"]/div[@class="seven columns"]/ul[@class="info"]/li[4]/text()').extract_first().split(' ')[0]
            if 'Property Type:' in li3:
                item['txn_type'] =i.xpath('div[@class="content"]/div[@class="seven columns"]/ul[@class="info"]/li[4]/text()').extract_first()

            if 'Property Type:' in li4:
                item['txn_type'] = i.xpath('div[@class="content"]/div[@class="seven columns"]/ul[@class="info"]/li[5]/text()').extract_first()

            try:
                list1 = i.xpath('div[@class="content"]/div[@class="seven columns"]/ul[@class="add-info"]/li[2]/div/span/text()').extract_first()
                list2 = i.xpath('div[@class="content"]/div[@class="seven columns"]/ul[@class="add-info"]/li[3]/div/span/text()').extract_first()
            except:
                print 'no problem'
            if 'Builder' in list1:
                item['listing_by'] = i.xpath('div[@class="content"]/div[@class="seven columns"]/ul[@class="add-info"]/li[2]/div/a/text()').extract_first()
            if 'Builder' in list2:
                item['listing_by'] = i.xpath('div[@class="content"]/div[@class="seven columns"]/ul[@class="add-info"]/li[3]/div/a/text()').extract_first()

            stat = i.xpath('div[@class="content"]/div[@class="seven columns"]/ul[@class="add-info"]/li[1]/span/text()').extract_first()
            if 'Furnished State' in stat:
                item['Status'] = i.xpath('div[@class="content"]/div[@class="seven columns"]/ul[@class="add-info"]/li[1]/text()').extract_first()

            item['Details'] = i.xpath('div[@class="footer"]/p/text()').extract_first()

            url = 'http://property.sulekha.com'+i.xpath('div[@class="header"]/div[@class="title"]/strong/a[@class="GAPListingTitle"]/@href').extract_first()

            yield Request(url,callback=self.parse1,dont_filter=True)

        curPage = int(response.url.split('-')[-1])

        try:
            nextPage = i.xpath('//div[@class="pagination"]/ul/li[last()]/a/@href').extract_first()
        except:
            maxPage = curPage + 1
            nextPage = '/property-in-mumbai-for-sale_page-'.format(x=str(maxPage))
        next_url = 'http://property.sulekha.com'+nextPage
        yield Request(next_url,callback=self.parse)

    def parse1(self , response):
        hxs = Selector(response)

        item = response.meta['item']
        


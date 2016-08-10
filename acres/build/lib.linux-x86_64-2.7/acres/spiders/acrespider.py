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
            'http://www.99acres.com/property-in-mumbai-ffid-page-1?orig_property_type=R&class=O,A,B&search_type=QS&search_location=CP12&lstacn=SEARCH&pageid=QS&search_id=7019357638975910&src=PAGING&lastAcn=SEARCH&lastAcnId=7019357638975910' , 
            'http://www.99acres.com/rent-property-in-mumbai-ffid-page-1?orig_property_type=R&class=O,A,B&search_type=QS&search_location=CP12&pageid=QS&search_id=7024716630429298&src=PAGING&lastAcn=SEARCH&lastAcnId=7024716630429298&fsl_results=Y&total_fsl_count=2'
            #'http://www.99acres.com/commercial-property-in-mumbai-ffid-page-1?orig_property_type=C&class=O,A,B&search_type=QS&search_location=SH&lstacn=SEARCH&pageid=QS&search_id=7025026338708533&src=PAGING&lastAcn=SEARCH&lastAcnId=7025026338708533&fsl_results=Y&total_fsl_count=2',
            #'http://www.99acres.com/rent-commercial-property-in-mumbai-ffid-page-1?orig_property_type=C&class=O,A,B&search_type=QS&search_location=SH&lstacn=SEARCH&pageid=QS&keyword_orig=mumbai&search_id=7025187469574654&src=PAGING&lastAcn=SEARCH&lastAcnId=7025187469574654&fsl_results=Y&total_fsl_count='
            ]
    custom_settings = {
            'BOT_NAME': 'acres',
            'DEPTH_LIMIT': 7000,
            'DOWNLOAD_DELAY': 5
        }
    #data_list = []
    def parse(self,response):
        hxs = Selector(response)
        path1 = "//div[@id='ysf']/h1"
        x1 = hxs.xpath(path1)
        path = "//div[@id='results']/div[1]/div[contains(@class,'srpWrap')]"
        x = hxs.xpath(path)
        
        for i in x:
            
            #if data_id not in self.data_list:
                try:
                    item = AcresItem()
                    #self.data_list.append(data_id)
                    data_id = i.xpath("@data-propid").extract_first()
                    sqft_check = i.xpath("div[@class='srpDetail']/div[@class='srpDataWrap']/span[1]/b[1]/text()").extract_first().replace("Sq.Ft.","").replace("Sq. Meter","").strip()
                    check = 0
                    #print sqft_check
                    if 'to' in sqft_check:
                        sqft1 = str(sqft_check.split('to')[0]).strip()
                        sqft2 = str(sqft_check.split('to')[1]).strip()
                        #print sqft1,sqft2
                        sqft_list = [sqft1,sqft2]
                        #print sqft_list
                    else:
                        sqft_list = [sqft_check]
                        #print sqft_list
                    for s in sqft_list:
                        check = check + 1    
                        item['data_id'] = data_id
                        item['platform'] = '99acres'
                        item['property_type'] = x1.xpath("span[@id='ysfPropertyType']/b/text()").extract_first().split(" ")[1]
                        item['txn_type'] = x1.xpath("span[2]/b/text()").extract_first()
                        item['city'] = x1.xpath("span[3]/b/text()").extract_first().split(" ")[0]
                    
                        item['Bua_sqft'] =  s
                        try:
                            item['price_per_sqft'] = i.xpath("div[@class='srpDetail']/div[@class='srpDataWrap']/span/text()").extract()[2].replace(' / Sq.Ft.','').strip()
                            #print item['price_per_sqft']
                            if item['price_per_sqft'] == '':
                                item['price_per_sqft'] = 'None'
                        except:
                            item['price_per_sqft'] = 'None'                         
                        try:
                            item['Building_name'] = str(i.xpath("div[@class='srpDetail']/div[@class='srpDataWrap']/span[2]/a[@class='sName']/b/text()").extract_first())
                        except:
                            try:
                                item['Building_name'] = str(i.xpath("div[@class='srpDetail']/div[@class='srpDataWrap']/span[2]/b/text()").extract_first())
                            except:
                                item['Building_name'] = 'None'
                        if item['Building_name'] == '':
                            item['Building_name'] = 'None'
                        
                        try:
                            age = i.xpath("div[@class='srpDetail']/div[@class='srpDataWrap']/span[3]/span[4]/text()").extract()[-1].strip()
                        except:
                            age = 'None'
                        try:
                            age1 = i.xpath("div[@class='srpDetail']/div[@class='srpDataWrap']/span[3]/span[3]/text()").extract()[-1].strip()
                        except:
                            age1 = 'None'
                        try:
                            age2 = i.xpath("div[@class='srpDetail']/div[@class='srpDataWrap']/span[2]/span[4]/text()").extract()[-1].strip()
                        except:
                            age2 = 'None'
                        try:
                            age3 = i.xpath("div[@class='srpDetail']/div[@class='srpDataWrap']/span[2]/span[3]/text()").extract()[-1].strip()
                        except:
                            age3 = 'None'
                        if (('years' in age) or ('year' in age) or ('old' in age)):
                            item['age'] = age
                        elif (('years' in age1) or ('year' in age1) or ('old' in age1)):
                            item['age'] = age1
                        elif (('years' in age2) or ('year' in age2) or ('old' in age2)):
                            item['age'] = age2
                        elif (('years' in age3) or ('year' in age3) or ('old' in age3)):
                            item['age'] = age3
                        else:
                            item['age'] = 'None'
                        
                        try:
                            poss = i.xpath("div[@class='srpDetail']/div[@class='srpDataWrap']/span[3]/span[4]/text()").extract()[-1].strip()
                            if 'Possession By' in poss:
                                poss = poss.replace('Possession By ','')
                                item['Possession'] = dt.strftime(dt.strptime(poss,'%b %Y'),'%m/%d/%Y %H:%M:%S')
                            else:
                                poss = i.xpath("div[@class='srpDetail']/div[@class='srpDataWrap']/span[2]/span[4]/text()").extract()[-1].strip()
                                if 'Possession By' in poss:
                                    poss = poss.replace('Possession By ','')
                                    item['Possession'] = dt.strftime(dt.strptime(poss,'%b %Y'),'%m/%d/%Y %H:%M:%S')
                                else:
                                    item['Possession'] = 'None'
                        except:
                            item['Possession'] = 'None'
                        
                        stat1 = str(i.xpath("div[@class='srpDetail']/div[@class='srpDataWrap']/span[3]/span/text()").extract()).replace('\\xa0','').replace('u','').replace(',','').replace("'","")
                        if 'Highlights:' in stat1:
                            item['Status'] = stat1
                        stat2 = str(i.xpath("div[@class='srpDetail']/div[@class='srpDataWrap']/span[2]/span/text()").extract()).replace('\\xa0','').replace('u','').replace(',','').replace("'","")
                        if 'Highlights:' in stat2:
                            item['Status'] = stat2
                        
                        detail1 = i.xpath("div[@class='srpDetail']/div[@class='srpDataWrap']/div[4]/b/text()").extract_first()
                        if 'Description :' in detail1:
                            item['Details'] = i.xpath("div[@class='srpDetail']/div[@class='srpDataWrap']/div[4]/text()").extract()[-1].strip()
                        else:
                            detail2 = i.xpath("div[@class='srpDetail']/div[@class='srpDataWrap']/div[3]/b/text()").extract_first()
                            if 'Description :' in detail2:
                                item['Details'] = i.xpath("div[@class='srpDetail']/div[@class='srpDataWrap']/div[3]/text()").extract()[-1].strip()
                        
                        if item['property_type'] == 'Residential':
                            conf1 = i.xpath("div[@class='wrapttl']/div[1]/a/text()").extract_first().split(',')[0]
                            conf2 = i.xpath("div[@class='wrapttl']/div[1]/a/text()").extract_first().split(')')[0].split('(')[-1]
                            if ('BHK' in conf1):
                                item['config_type'] = conf1
                            elif ('RK' in conf2):
                                item['config_type'] = conf2
                            elif 'Bedroom' in conf1:
                                item['config_type']  = conf1.split(" ")[0] + ' BHK'
                            else:
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
                                #print price1 , price2
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
                            if ((item['txn_type'] in 'On Rent') or (item['txn_type'] in 'Lease')):
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
                        item['address'] = 'None'
                        item['sublocality'] = 'None'
                        item['google_place_id'] = 'None'
                        item['Launch_date'] = 'None'
                        item['mobile_lister'] = 'None'
                        item['areacode'] = 'None'
                        item['management_by_landlord'] = 'None'
                        item['carpet_area'] = 'None'
                        item['updated_date'] = item['listing_date']
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
                except Exception:
                        print Exception

        curPage = int(response.url.split('?')[0].split('-')[-1])
        maxPage = str(response.xpath("//div[@class='lcol_new']/div[@class='pgdiv']/a[last()-1]/text()").extract_first())
        if maxPage == 'None':
            maxPage = curPage
        #print maxPage
        #print response.body
        if curPage <= maxPage :
            if 'rent-property' in response.url:
                next_url = 'http://www.99acres.com/rent-property-in-mumbai-ffid-page-{x}?orig_property_type=R&class=O,A,B&search_type=QS&search_location=CP12&pageid=QS&search_id=7024716630429298&src=PAGING&lastAcn=SEARCH&lastAcnId=7024716630429298&fsl_results=Y&total_fsl_count=2'.format(x=str(curPage+1))
                yield Request(next_url,callback=self.parse)
            else:
                if 'property' in response.url:
                    next_url = 'http://www.99acres.com/property-in-mumbai-ffid-page-{x}?orig_property_type=R&class=O,A,B&search_type=QS&search_location=CP12&lstacn=SEARCH&pageid=QS&search_id=7019357638975910&src=PAGING&lastAcn=SEARCH&lastAcnId=7019357638975910'.format(x=str(curPage+1))
                    yield Request(next_url,callback=self.parse)
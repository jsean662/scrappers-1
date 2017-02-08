# -*- coding: utf-8 -*-
import scrapy
from scrapy.selector import Selector
from ..items import AireaaagentsItem
from scrapy.http import Request
from datetime import datetime as dt


class AgentsaireaaSpider(scrapy.Spider):
    name = "agentsAireaa"
    allowed_domains = ["aireaa.com"]
    start_urls = [
        'http://aireaa.com/agent.php?page=%s&pr_keyword=&pr_protype=&pr_city=state_2&find_project=Find Agent/' % page for page in range(1, 1035)
    ]
    custom_settings = {
        'DEPTH_LIMIT': 10000,
        'DOWNLOAD_DELAY': 1
    }
    pageno = 1

    def parse(self, response):

        item = AireaaagentsItem()
        record = Selector(response)

        data = record.xpath('//div[@class="clbeat"]')

        localities = data_id = data_link = contact_person = company_name = ''

        for i in data:
            try:
                data_link = i.xpath('.//a[contains(@href,"agent_detail")]/@href').extract_first()
                data_id = data_link.split('id=')[1].split('=')[0].strip()
                # print(data_link)
                try:
                    company_name = i.xpath('.//div/div[2]/div[1]/h1/text()').extract_first()
                    # print(company_name)
                    contact_person = i.xpath('.//div/div[2]/div[2]/div/h2/text()').extract_first()
                    # print(contact_person)
                    localities = i.xpath('.//div/div[2]/div[1]/p/text()').extract_first()
                    # print(localities)
                except Exception as e:
                    print(e)

                item['data_id'] = data_id
                item['contact_person'] = contact_person.strip()
                item['company_name'] = company_name.strip()
                item['locality'] = localities.strip()
                item['platform'] = 'Aireaa'
                item['scraped_time'] = dt.now().strftime('%m/%d/%Y %H:%M:%S')

                url = 'http://aireaa.com/' + data_link

                request = Request(url, callback=self.parse1, dont_filter=True, meta={'item': item})

                yield request

            except Exception as e:
                print(e)

            '''if self.pageno <= 1305:
                self.pageno += 1
                next_url = 'http://aireaa.com/agent.php?page=' + str(self.pageno) + '&pr_keyword=&pr_protype=&pr_city=state_2&find_project=Find%20Agent'
                yield Request(next_url, callback=self.parse)'''

    def parse1(self, response):
        try:
            # item['city'] = 'Mumbai'
            # item['platform'] = 'Aireaa'
            # item['scraped_time'] = dt.now().strftime('%m/%d/%Y %H:%M:%S')
            # item['data_id'] = response.meta['data_id']
            # item['contact_person'] = response.meta['contact_person']
            # item['company_name'] = response.meta['company_name']
            # item['locality'] = response.meta['locality']
            item = response.meta['item']

            list = response.xpath('//*[@id="out_pro"]/div/div/div[1]/div[@class="lt"]/text()').extract()
            data = response.xpath('//*[@id="out_pro"]/div/div/div[1]/div[@class="rt"]/text()').extract()
            data2 = response.xpath('//*[@id="out_pro"]/div/div/div[1]/div[@class="rt"]/a/@href').extract()

            item['city'] = data[0]
            if 'All' in item['city']:
                item['city'] = item['city'].split('(')[0].strip()

            if 'Mobile Number:' in list:
                item['mobile_no'] = data[1].strip()

            if 'Phone Number:' in list:
                item['phone_no'] = data[2].strip()

            if 'Email Address:' in list:
                item['email_id'] = data2[0].split(':')[1].strip()

            if 'Website:' in list:
                item['website'] = data2[1].strip()

            if 'Phone Number:' not in list and 'Address:' in list:
                item['address'] = data[2].strip() + data[3].strip()
            elif 'Address:' in list and 'Phone Number:' in list:
                item['address'] = data[3].strip() + data[4].strip()

                item['address'] = item['address'].strip()

            if item['locality'] == '' or item['locality'] == ' ':
                item['locality'] = 'None'

            '''try:
                geolink = response.xpath('//*[@id="out_pro"]/div/div/div[2]/iframe/@src').extract_first()

                if geolink is not None:
                    request = Request(geolink, callback=self.parse2, dont_filter=True, meta={'item': item})
                    # request.meta['data_id'] = data_id
                    yield request
            except Exception as e:
                print(e)'''
            yield item
        except Exception as e:
            print(e)


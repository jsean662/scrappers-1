# -*- coding: utf-8 -*-
import scrapy
from ..items import BsemembersItem
from scrapy.selector import Selector
from datetime import datetime
from scrapy.http import Request


class BseagentsspiderSpider(scrapy.Spider):
    name = "BSESpider"
    allowed_domains = ["www.bseindia.com"]
    start_urls = [
        'http://www.bseindia.com/members/Memberdata.aspx?MemberNo=%s' % page for page in range(1, 6662)
    ]
    custom_settings = {
        'DOWNLOAD_DELAY': 3.0,
    }

    def parse(self, response):
        item = BsemembersItem()
        record = Selector(response)

        item['data_id'] = record.xpath('//*[@id="ctl00_ContentPlaceHolder1_tdData"]/table/tr[1]/td[2]/text()').extract_first()

        if item['data_id'] == None:
            pass
        else:
            item['company_member_list'] = []
            item['company_name'] = record.xpath('//span[@id="ctl00_ContentPlaceHolder1_lblMembername"]/text()').extract_first()
            members = len(response.xpath('*//td[contains(text(),"Old Name")]/text()').extract())

            if members is not None or not members == 0:
                for member in range(2, members+2):
                    item['company_member_list'].append(record.xpath('//div[@id="ctl00_ContentPlaceHolder1_tdData"]/table/tr[' + str(member) + ']/td[2]/text()').extract_first())

                item['registered_office_address'] = record.xpath('//*[@id="ctl00_ContentPlaceHolder1_tdData"]/table/tr[' + str(members+3) + ']/td[2]/text()').extract()
                item['correspondence_address'] = record.xpath('//*[@id="ctl00_ContentPlaceHolder1_tdData"]/table/tr[' + str(members+3) + ']/td[2]/text()').extract()

                item['office_contact_no'] = record.xpath('//*[@id="ctl00_ContentPlaceHolder1_tdData"]/table/tr[' + str(members+4) + ']/td[2]/text()').extract()
                item['correspondence_contact_no'] = record.xpath('//*[@id="ctl00_ContentPlaceHolder1_tdData"]/table/tr[' + str(members+4) + ']/td[4]/text()').extract()

                item['office_fax'] = record.xpath('//*[@id="ctl00_ContentPlaceHolder1_tdData"]/table/tr[' + str(members+5) + ']/td[2]/text()').extract()
                item['correspondence_fax'] = record.xpath('//*[@id="ctl00_ContentPlaceHolder1_tdData"]/table/tr[' + str(members+5) + ']/td[4]/text()').extract()

                item['email_id'] = record.xpath('//*[@id="ctl00_ContentPlaceHolder1_tdData"]/table/tr[' + str(members+6) + ']/td[2]/text()').extract()
                item['website'] = record.xpath('//*[@id="ctl00_ContentPlaceHolder1_tdData"]/table/tr[' + str(members+6) + ']/td[4]/text()').extract()

                item['SEBI_Registration_no'] = record.xpath('//*[@id="ctl00_ContentPlaceHolder1_tdData"]/table/tr[' + str(members+8) + ']/td[2]/text()').extract_first()
                item['SEBI_Registration_date'] = record.xpath('//*[@id="ctl00_ContentPlaceHolder1_tdData"]/table/tr['+ str(members+8)+ ']/td[4]/text()').extract_first()

                item['Chief_Executive_Name'] = record.xpath('//*[@id="ctl00_ContentPlaceHolder1_tdData"]/table/tr['+ str(members+19) +']/td[2]/text()[1]').extract_first()
                item['Chief_Executive_Phone'] = record.xpath('//*[@id="ctl00_ContentPlaceHolder1_tdData"]/table/tr['+ str(members+20) +']/td[2]/text()').extract_first()
                item['Chief_Executive_Email'] = record.xpath('//*[@id="ctl00_ContentPlaceHolder1_tdData"]/table/tr['+ str(members+19) +']/td[2]/text()[last()]').extract_first()

                item['Board_Member_Links'] = record.xpath('//*[@id="ctl00_ContentPlaceHolder1_tdData"]/table/tr[' + str(members+19) + ']/td[2]/table/tr/td/a/@href').extract()
                # '//*[@id="ctl00_ContentPlaceHolder1_tdData"]/table/tbody/tr[20]/td[2]/table/tbody/tr[2]/td[1]/a'
                item['scraped_time'] = datetime.now().strftime('%m/%d/%Y')
                if item['Board_Member_Links']:
                    for link in item['Board_Member_Links']:
                        url = 'http://www.bseindia.com/members/' + link.split('&City=')[0] + '&City='
                        request = Request(url, callback=self.membervisit, dont_filter=False)
                        request.meta['item'] = item
                        yield request
                else:
                    item['Board_Member_Links'] = []
                yield item
        
    def membervisit(self, response):
        item = response.meta['item']
        item['Board_Member_Name'] = response.xpath('//*[@id="ctl00_ContentPlaceHolder1_tdData"]/table/tr[1]/td/b/text()').extract_first().split(': ')[1]
        item['Board_Member_Position'] = response.xpath('//*[@id="ctl00_ContentPlaceHolder1_tdData"]/table/tr[3]/td/table/tr[4]/td[2]/text()').extract_first()
        item['Board_Member_Email'] = response.xpath('//*[@id="ctl00_ContentPlaceHolder1_tdData"]/table/tr[3]/td/table/tr[3]/td[2]/text()').extract_first()
        yield item
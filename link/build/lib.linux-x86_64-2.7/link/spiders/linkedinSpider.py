
from scrapy.http import FormRequest
from link.items import LinkItem
from scrapy.spiders import Spider
import json
import time
from scrapy.selector import Selector
from scrapy.http import Request
from scrapy.utils.response import open_in_browser


class LinkedinSpider(Spider):
    name = "linkedin"
    allowed_domains = ["linkedin.com"]
    start_urls = ["https://www.linkedin.com/uas/login"]
    custom_settings = {
        'DEPTH_LIMIT' : 1000,
        'DOWNLOAD_DELAY' : 3
    }

    def parse(self, response):
        formdata = {'session_key': 'karanchudasama1@gmail.com',
                'session_password': 'K@r@N#25#10#94' }
        yield FormRequest.from_response(response,
                                        formdata=formdata,
                                        clickdata={'name': 'signin'},
                                        callback=self.parse1)

    def parse1(self, response):
        url = 'https://www.linkedin.com/vsearch/p?keywords=financial+analyst&distance=50&pt=people&postalCode=400058&locationType=I&rsid=4975470201469512657697&page_num=1&orig=ADVS&countryCode=in&openAdvancedForm=true'
        yield Request(url,callback = self.parse_items)

    def parse_items(self,response):
        #open_in_browser(response)
        hxs = Selector(response)
        #print response.body
    
        data =  hxs.xpath("//code[@id='voltron_srp_main-content']/text()").extract()
        #print data
        data = data[0].replace("\u002d1","2")
        #print data
        jsndata = json.loads(data.split("--")[-2])
        #print jsndata
        path =  jsndata['content']['page']['voltron_unified_search_json']['search']['results']
        
        pageNo = int(response.url.split('=')[-4].split('&')[0])
        #print pageNo
        
        for i in range(1,11):
            item = LinkItem()
            try:
                item['name'] = path[i]['person']['fmt_name']
            except:
                item['name'] = 'No name'
            item['position'] = path[i]['person']['snippets'][0]['heading'].split('at ')[0].replace('<','').replace('>','').replace('B','').replace('/','')
            item['company'] = path[i]['person']['snippets'][0]['heading'].split('at ')[-1]
            yield item

        next_url = 'https://www.linkedin.com/vsearch/p?keywords=financial+analyst&distance=50&pt=people&postalCode=400058&locationType=I&rsid=4975470201469512657697&page_num={x}&orig=ADVS&countryCode=in&openAdvancedForm=true'.format(x=str(pageNo+1))
        time.sleep(4)
        yield Request(next_url,callback=self.parse_items)
        #path = response.xpath('.')#//ol[@id="results"]')
        #item = LinkItem()
        #item['name'] = path
        '''for i in path:
            item = LinkItem()

            item['name'] = i.xpath('div[@class="bd"]/h3/a/text()').extract_first()
            item['position'] = str(i.xpath('div[@class="bd"]/dl[2]/dd/p/b[1]/text()').extract_first()) + str(i.xpath('div[@class="bd"]/dl[2]/dd/p/b[2]/text()').extract_first())

            comp = i.xpath('div[@class="bd"/dl[2]/dd/p/text()').extract_first()
            if 'at' in comp:
                item['company'] = comp.split('at')[-1]

            yield item'''

'''import scrapy
from scrapy.spiders import Spider
from scrapy.selector import Selector
from scrapy.http import Request
from scrapy.http import FormRequest
from scrapy.utils.response import open_in_browser

class Formfill(scrapy.Spider):
    name = 'form'
    
    allowed_domains = ['linkedin.com']
    start_urls = ['https://www.linkedin.com/uas/login']
    
    def parse(self,response):
        
        formdata = {'session_key': 'karanchudasama1@gmail.com',
                'session_password': 'K@r@N#25#10#94' }
        yield FormRequest.from_response(response,
                                        formdata=fromdata,
                                        clickdata={'name' : 'signin'},
                                        callback=self.parse1)
                                        
    def parse1(self, response):
        open_in_browser(response)'''                                    

from scrapy.item import Item, Field
from scrapy.http import FormRequest
from formfill.items import FormfilldataItem
from scrapy.spider import Spider
from scrapy.selector import Selector
from scrapy.http import Request
from scrapy.utils.response import open_in_browser


class GitSpider(Spider):
    name = "github"
    allowed_domains = ["linkedin.com"]
    start_urls = ["https://www.linkedin.com/uas/login"]

    def parse(self, response):
        formdata = {'session_key': 'karanchudasama1@gmail.com',
                'session_password': 'K@r@N#25#10#94' }
        yield FormRequest.from_response(response,
                                        formdata=formdata,
                                        clickdata={'name': 'signin'},
                                        callback=self.parse1)

    def parse1(self, response):
        url = 'https://www.linkedin.com/vsearch/p?keywords=financial%20analyst&postalCode=400058&openAdvancedForm=true&locationType=I&countryCode=in&distance=50&rsid=4975470201469512657697&orig=ADVS&page_num=1&pt=people'
        yield Request(url,callback = self.parse_items)

    def parse_items(self,response):
        open_in_browser(response)
        hxs = Selector(response)

        path = hxs.xpath('.//div[@id="results-container"]/ol[@id="results"]/li[contains(@class,"mod result ")]')

        for i in path:
            item = FormfillItem()

            item['name'] = i.xpath('div[@class="bd"]/h3/a/text()').extract_first()
            item['position'] = str(i.xpath('div[@class="bd"]/dl[2]/dd/p/b[1]/text()').extract_first()) + str(i.xpath('div[@class="bd"]/dl[2]/dd/p/b[2]/text()').extract_first())

            comp = i.xpath('div[@class="bd"/dl[2]/dd/p/text()').extract_first()
            if 'at' in comp:
                item['company'] = comp.split('at')[-1]

            yield item

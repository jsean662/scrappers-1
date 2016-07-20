import scrapy
import time
from scrap.items import ScrapItem
from scrapy.selector import Selector
import re
from scrapy.http import Request

class DmozSpider(scrapy.Spider):
    name = "dmoz"
    allowed_domains = ["dmoz.org"]
    #base_urls = "https://twitter.com"
    start_urls = [ 'https://twitter.com/abodesindia']
    
    #for post in ('ESTATEMUMBAI','zabrickportal','vijayrealtor','abodesindia','RealtyCable'):
     #   start_urls.append(base_urls+"/"+post+"/")
    
    
    def parse(self, response):
        
        hxs = Selector(response)
        base_url = 'https://twitter.com'
        #number =  (response.xpath('//li[contains(@id,"stream-item-tweet-")]').re(r'id="stream-item-tweet-(\d{18})"'))
        #url = "https://twitter.com/abodesindia/status/"+
        #post_no = response.xpath('//li[@class="ProfileNav-item ProfileNav-item--tweets is-active"]/a/span[2]/text()').extract()
        #post = int(float(str(post_no[0]).replace("K",""))*1000)
        li = hxs.xpath("//li/div/div[2]")
        for path in li:
            #base_url = 'https://twitter.com'
            #time.sleep(2)
            #number =  (response.xpath('//li[contains(@id,"stream-item-tweet-")]').re(r'id="stream-item-tweet-(\d{18})"'))
            #li1 = li.xpath('li[contains(@id,"stream-item-tweet-{number}")]')
            #print li1
            item = ScrapItem()
            item['content'] = path.xpath('div[2]/p/text()').extract()
            item['time'] = path.xpath('div[1]/small/a/@title').extract()
            yield item
            #url = base_url + str(li1)
            
            #print url
        
            #yield Request(url, callback=self.parse )                              
             

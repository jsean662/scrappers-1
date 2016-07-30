import scrapy
from fip_contact.items import FipContactItem
from scrapy.spiders import Spider
from scrapy.spiders import CrawlSpider, Rule
from scrapy.selector import Selector
from scrapy.http import Request


class FipSpider(scrapy.Spider):
	name = 'FipConSpider'
	allowed_domains = ['fipindia.com']

	start_urls = ['http://fipindia.com/members.asp?pagest=1&mem_type=ORDINARY&mem_fullname=' , 
				  'http://fipindia.com/members.asp?pagest=1&mem_type=LIFE&mem_fullname=' ]

	custom_settings = {
        'DEPTH_LIMIT' : 1000,
        'DOWNLOAD_DELAY' : 2
    }

	def parse(self , response):
		hxs = Selector(response)

		pageNo = int(response.url.split("=")[1].split("&")[0])
		#print pageNo
		#if 'ORDINARY' in response.url

		path = hxs.xpath('.//div[@class="row"]/div[@class="grid_4"]')
		print path , len(path)

		for i in path:
			item = FipContactItem()

			item['name'] = i.xpath('strong[1]/text()').extract_first()
			item['airline'] = i.xpath('strong[3]/text()').extract_first()

			yield item

		nextPage = pageNo + 15
		if ('ORDINARY' in str(response.url)) and (nextPage < 1739):
			next_url = 'http://fipindia.com/members.asp?pagest='+str(nextPage)+'&mem_type=ORDINARY&mem_fullname='
			yield Request(next_url,self.parse)
		if ('LIFE' in str(response.url)) and (nextPage < 1500):
			next_url = 'http://fipindia.com/members.asp?pagest='+str(nextPage)+'&mem_type=LIFE&mem_fullname='
			yield Request(next_url,self.parse)

import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.selector import HtmlXPathSelector
from scrapy.http import Request
from scrapy.linkextractors import LinkExtractor
from scrapy.selector import Selector
from abode.items import AbodeItem
from scrapy.loader import ItemLoader

class abodeSpider(CrawlSpider):
	name = "abode"
	allowed_domains = ["abodesindia.com"]
	start_urls = [
        "http://www.abodesindia.com/property-for-sale-all-residential-in-mumbai/1101"
    ]
	rules = (Rule(LinkExtractor(deny=(), allow=('http://www.abodesindia.com/'), ), callback='parse_item', follow=True, ),)
	custom_settings = {
            'BOT_NAME': 'abode-scraper',
            'DEPTH_LIMIT': 1000,
            'DOWNLOAD_DELAY': 0
        }
        #^(.*?(mumbai)[^$]*)$
        #restrictxpaths in link extractorwww.abodesindia.com/
	def parse_item(self, response):
		#items = []
#		plinks = Selector(text=response.body).xpath("//div")
#		print plinks
		#plinks={}
		
		#l = ItemLoader(item=AbodeItem(),response=response)
 #       	l.default_input_processor = MapCompose(lambda v: v.split(), replace_escape_chars)
#	        l.default_output_processor = Join()
#		l.add_value('idx', i)
		#l.add_xpath('desc', "//h1[contains(concat(' ',normalize-space(@itemprop),' '),' description ')]/text()")
        	#yield l.load_item()
        

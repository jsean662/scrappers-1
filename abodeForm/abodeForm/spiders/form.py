from scrapy.http import FormRequest
from scrapy.spiders import Spider
from scrapy.http import Request
from selenium import webdriver
from scrapy.utils.response import open_in_browser
from scrapy.linkextractors import LinkExtractor

class Abodeform(Spider):
	name = 'abodeFormSpider'
	allowed_domains = ['abodesindia.com']
	start_urls = ['http://www.abodesindia.com/signin.asp?websiteid=']

	#rules = (Rule(LinkExtractor(deny=(), allow=('http://www.abodesindia.com/'), ), callback='parse1', follow=True, ),)

	def parse(self,response):
		formdata1 = { 'loginname':'nexchanges.market@gmail.com' ,
					  'pwd' : 'NMPLbhavans123'

					}
		yield FormRequest.from_response(response,
                                        formdata=formdata1,
                                        clickdata={'name': 'submit1'},
                                        callback=self.parse1)

	def parse1(self,response):
		new = response.xpath('.//a[@href="/resi/SpeedListingForm.asp"]/@href').extract_first()
		url = 'http://www.abodesindia.com'+new
		yield Request(url,callback=self.parse2)
		#print response.body
		#open_in_browser(response)

	def parse2(self,response):
		formdata2 = { 'tpc' : 'R' ,
					  'pfl' : '748' ,
					  'formcode' : '0' ,
					  'mainpropowner' : 'I' ,
					  'clientcode' : '0' , 
					  'prop_age' : 'N' ,
					  'poss_month' : 'August ' , 
					  'poss_year' : '2016' , 
					}
		yield FormRequest.from_response(response,
										formdata=formdata2,
										clickdata={ 'name' : 'Submit'},
										callback=self.parse3,dont_filter=True)

	def parse3(self,response):
		print response.body
		open_in_browser(response) #http://www.abodesindia.com/shared/listProperty_pre.asp?websiteid=
								  #http://www.abodesindia.com/shared/listpropertycrm.asp?propcode=RS1084638&websiteid=&rcode=N
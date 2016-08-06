from scrapy.http import FormRequest
from scrapy.spiders import Spider
from scrapy.http import Request
from selenium import webdriver
from scrapy.utils.response import open_in_browser
from scrapy.linkextractors import LinkExtractor

class QuikrFormSpider(Spider):
	name = 'quikr'
	allowed_domains = ['quikr.com']
	start_urls = ['http://www.quikr.com/homes/postad']

	def parse(self , response):
		formdata = {
		'user_type' : '2' ,
		'ad_type' : '1' ,
		'adCities' : 'Mumbai' ,
		'adProject' : 'Malad East' ,
		'property_area' : '300' ,
		'sellingPrice' : '2500000' ,
		'squareFtPrice' : '8500' ,
		'adTitle' : 'Spacious 1BHK flat in malad with parking facility' ,
		'adDesc' : 'Property is available immediate and it is near to western express highway' , 
		'user_name' : 'pratham' ,
		'email' : 'prathamsawant115@gmail.com' ,
		'phone' : '9004074337'
		}

		yield FormRequest.from_response(response,
										formdata=formdata,
										clickdata={ "ng-class" : "{active:PostAdTree.AboutPropertySection.subsections.Property_Type.value == 'Apartment'}" , 
													"ng-class" : "{active:PostAdTree.AboutPropertySection.subsections.Property_Details.subsections.bhk.value==key}" ,
													"ng-class" : "{disabled : value.autoFilled && pageType!='EAP'}" , 
													"ng-click" : "papSaveCall()",
										},
										callback=self.parse1
										)

	def parse1(self , response):
		print response.body
		open_in_browser(response)
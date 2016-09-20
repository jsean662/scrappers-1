from scrapy.spiders import CrawlSpider
from selenium import webdriver
import os
from scrapy.http import FormRequest
from makaanform.items import MakaanformItem
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from scrapy.selector import Selector
from scrapy.utils.response import open_in_browser
import time
#import pymongo

class Makaan(CrawlSpider):
	name = 'posting'
	allowed_domains = ['makaan.com']

	start_urls = ['https://oyeok.in']

	item = MakaanformItem()

	def __init__(self):
		self.driver = webdriver.Chrome()

	def parse(self , response):
		self.driver.get('https://oyeok.in')
		self.driver.implicitly_wait(20)

		print self.driver.page_source

		no = self.driver.find_element_by_xpath('//div[@id="branch-sms-block"]/form/input[@id="branch-sms-phone"]')
		no.send_keys('+918976551754')


		time.sleep(10)
		self.driver.quit()
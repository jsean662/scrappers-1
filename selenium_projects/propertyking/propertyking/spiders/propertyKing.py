from scrapy.spiders import CrawlSpider
from selenium_projects import webdriver
import os
from scrapy.http import FormRequest
from selenium_projects.webdriver.common.keys import Keys
from selenium_projects.webdriver.common.action_chains import ActionChains
from scrapy.selector import Selector
from scrapy.utils.response import open_in_browser
import datetime
import time
import pymongo
from scrapy import log

class PropertyKing(CrawlSpider):
	name = 'propertyKingPub'
	start_urls = ['http://propertyking.club/']

	def __init__(self):
		self.driver = webdriver.Chrome()
		MONGODB_SERVER = "localhost"
		MONGODB_PORT = 27017
		# MONGODB_DB = "scraping"
		# MONGODB_COLLECTION = "scrape"
		connection = pymongo.MongoClient(MONGODB_SERVER,MONGODB_PORT)
		db = connection['scraping']
		self.collection_a = db['andheri']
		self.collection_p = db['post']

	def parse(self,response):
		add = 0
		data_post = list(self.collection_a.find().limit(1))

		for i in range(0,len(data_post)):
			if (i%8==0):
				add = add + 1000
			if (not i==0):
				self.__init__()
			self.driver.get(response.url)
			self.driver.implicitly_wait(50)
			time.sleep(10)

			login_clc = self.driver.find_element_by_id('login_open').click()
			self.driver.implicitly_wait(50)
			time.sleep(5)

			if i%8==0:
				email = self.driver.find_element_by_id('email')
				email.send_keys('oyeok.realestate2@gmail.com')
				self.driver.implicitly_wait(50)
				time.sleep(5)
			if i%8==1:
				email = self.driver.find_element_by_id('email')
				email.send_keys('')
				self.driver.implicitly_wait(50)
				time.sleep(5)

			passw = self.driver.find_element_by_id('password')
			passw.send_keys('nx1234')
			self.driver.implicitly_wait(50)
			time.sleep(5)

			log_butn = self.driver.find_element_by_xpath('//button[@type="submit"]').click()
			self.driver.implicitly_wait(50)
			time.sleep(5)

			publish = self.driver.find_element_by_xpath('//a[@class="btn btn-success"]').click()
			self.driver.implicitly_wait(50)
			time.sleep(5)

			catgry = self.driver.find_element_by_xpath('//select[@id="catId"]/option[@value="5"]').click()
			self.driver.implicitly_wait(50)
			time.sleep(5)

			title = self.driver.find_element_by_id('titleen_US')
			title.send_keys(data_post[i]['title'])
			self.driver.implicitly_wait(50)
			time.sleep(5)

			desc = self.driver.find_element_by_id('descriptionen_US')
			desc.send_keys(data_post[i]['detail'])
			self.driver.implicitly_wait(50)
			time.sleep(5)

			if '.' in data_post[i]['rent_price']:
				data_post[i]['rent_price'] = data_post[i]['rent_price'].split('.')[0]
				data_post[i]['rent_price'] = str(int(data_post[i]['rent_price'])+add)
			else:
				data_post[i]['rent_price'] = str(int(data_post[i]['rent_price'])+add)
			price = self.driver.find_element_by_id('price')
			price.send_keys(data_post[i]['rent_price'])
			self.driver.implicitly_wait(50)
			time.sleep(5)

			img = self.driver.find_element_by_name('qqfile')
			img.send_keys('/home/karan/scrap_proj/selenium_projects/Postings_photos/live.jpg')
			self.driver.implicitly_wait(50)
			time.sleep(10)

			cntry = self.driver.find_element_by_xpath('//select[@id="countryId"]/option[@value="IN"]').click()
			self.driver.implicitly_wait(50)
			time.sleep(5)

			state = self.driver.find_element_by_xpath('//select[@id="regionId"]/option[@value="781510"]').click()
			self.driver.implicitly_wait(50)
			time.sleep(5)

			city = self.driver.find_element_by_xpath('//select[@id="cityId"]/option[@value="278320"]').click()
			self.driver.implicitly_wait(50)
			time.sleep(5)

			cty_area = self.driver.find_element_by_id('cityArea')
			cty_area.send_keys(data_post[i]['locality'])
			self.driver.implicitly_wait(50)
			time.sleep(5)

			subt = self.driver.find_element_by_xpath('//button[@type="submit"]').click()
			self.driver.implicitly_wait(50)
			time.sleep(60)

			time.sleep(5)
			self.driver.quit()
			time.sleep(20)
			if i%5==0:
				time.sleep(30)
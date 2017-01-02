from scrapy.spiders import CrawlSpider
from selenium import webdriver
import os
from scrapy.http import FormRequest
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from scrapy.selector import Selector
from scrapy.utils.response import open_in_browser
import datetime
import time
import pymongo


class SulekhaPost(CrawlSpider):
	name = 'sulekhapost'
	allowed_domains = ['sulekha.com']
	start_urls = ['http://property.sulekha.com/post-your-property']
	
	#'locality':'','sub_loc':'','sqft':'','rent_price':'','title':'','detail':'','bed':'','flr':'','t_flr':'','depo':'','status':'','email':''

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
		data_post = list(self.collection_a.find().limit(5))
		#print data_post

		for i in range(0,len(data_post)):
			if i%2==0:
				add = add + 1000
			if (not i==0):
				self.__init__()
			self.driver.get(response.url)
			self.driver.implicitly_wait(40)
			self.driver.maximize_window()
			self.driver.implicitly_wait(50)
			time.sleep(2)

			login = self.driver.find_element_by_id('sul_ressignin').click()
			self.driver.implicitly_wait(40)
			time.sleep(2)

			self.driver.switch_to.frame(self.driver.find_element_by_tag_name('iframe'))

			if (i%2==0):
				email = self.driver.find_element_by_id('txtuname')
				email.send_keys('prathamsawant115@gmail.com')
				self.driver.implicitly_wait(20)
				time.sleep(2)
			if (i%2==1):
				email = self.driver.find_element_by_id('txtuname')
				email.send_keys('vipulmalhotra511@gmail.com')
				self.driver.implicitly_wait(20)
				time.sleep(2)

			passw = self.driver.find_element_by_id('txtpwd')
			passw.send_keys('nx1234')
			self.driver.implicitly_wait(20)
			time.sleep(2)

			sign = self.driver.find_element_by_id('btnsignin').click()
			self.driver.implicitly_wait(20)
			time.sleep(5)

			prop = self.driver.find_element_by_xpath('//div[@class="inner-group"]/ul/li[1]')
			act_prop = ActionChains(self.driver)
			act_prop.move_to_element(prop)
			act_prop.click(prop).perform()
			self.driver.implicitly_wait(20)
			time.sleep(2)

			scroll = self.driver.execute_script('window.scrollTo(0,500);')
			self.driver.implicitly_wait(10)

			rent = self.driver.find_element_by_xpath('//div[@class="form-group"]/div[@class="manage-menu tabs"]/ul/li[@data-value="Rentals"]/a').click()
			self.driver.implicitly_wait(20)
			time.sleep(3)

			proc = self.driver.find_element_by_xpath('//div[@class="action"]/a').click()
			self.driver.implicitly_wait(20)
			time.sleep(2)

			loc = self.driver.find_element_by_xpath('//div[@class="google-maps maperror"]/div[@class="search-box"]/input')
			self.driver.implicitly_wait(20)
			loc.send_keys(data_post[i]['sub_loc'])
			self.driver.implicitly_wait(20)
			time.sleep(2)

			if 'carter' in data_post[i]['locality']:
				loction = self.driver.find_element_by_xpath('//div[@id="locationdrop"]/span/input[2]')
				loction.send_keys('bandra west ')
				self.driver.implicitly_wait(20)
				time.sleep(2)
			else:
				loction = self.driver.find_element_by_xpath('//div[@id="locationdrop"]/span/input[2]')
				loction.send_keys(data_post[i]['locality'])
				self.driver.implicitly_wait(20)
				time.sleep(2)

			super_built = self.driver.find_element_by_id('txtSuperBuiltupArea')
			super_built.send_keys(data_post[i]['sqft'])
			self.driver.implicitly_wait(20)
			time.sleep(2)
			
			if '1' in data_post[i]['bed']:
				bed = self.driver.find_element_by_xpath('//div[@data-for="bedrooms"]/div/ul/li[1]').click()
				self.driver.implicitly_wait(20)
				time.sleep(2)
			elif '2' in data_post[i]['bed']:
				bed = self.driver.find_element_by_xpath('//div[@data-for="bedrooms"]/div/ul/li[2]').click()
				self.driver.implicitly_wait(20)
				time.sleep(2)
			elif '3' in data_post[i]['bed']:
				bed = self.driver.find_element_by_xpath('//div[@data-for="bedrooms"]/div/ul/li[3]').click()
				self.driver.implicitly_wait(20)
				time.sleep(2)
			elif '4' in data_post[i]['bed']:
				bed = self.driver.find_element_by_xpath('//div[@data-for="bedrooms"]/div/ul/li[4]').click()
				self.driver.implicitly_wait(20)
				time.sleep(2)

			if '1' in data_post[i]['bed']:
				bed = self.driver.find_element_by_xpath('//div[@data-for="bathroom"]/div/ul/li[1]').click()
				self.driver.implicitly_wait(20)
				time.sleep(2)
			elif '2' in data_post[i]['bed']:
				bed = self.driver.find_element_by_xpath('//div[@data-for="bathroom"]/div/ul/li[2]').click()
				self.driver.implicitly_wait(20)
				time.sleep(2)
			elif '3' in data_post[i]['bed']:
				bed = self.driver.find_element_by_xpath('//div[@data-for="bathroom"]/div/ul/li[3]').click()
				self.driver.implicitly_wait(20)
				time.sleep(2)
			elif '4' in data_post[i]['bed']:
				bed = self.driver.find_element_by_xpath('//div[@data-for="bathroom"]/div/ul/li[4]').click()
				self.driver.implicitly_wait(20)
				time.sleep(2)

			if 'Semi-Furnished' in data_post[i]['status']:
				stat = self.driver.find_element_by_xpath('//div[@data-for="furnishing-type"]/div/ul/li[2]').click()
				self.driver.implicitly_wait(20)
				time.sleep(2)

				st1 = self.driver.find_element_by_xpath('//div[@id="divFurnishedInfo"]/div/ul/li[2]').click()
				self.driver.implicitly_wait(20)
				time.sleep(2)

				st2 = self.driver.find_element_by_xpath('//div[@id="divFurnishedInfo"]/div/ul/li[3]').click()
				self.driver.implicitly_wait(20)
				time.sleep(2)

				st3 = self.driver.find_element_by_xpath('//div[@id="divFurnishedInfo"]/div/ul/li[4]').click()
				self.driver.implicitly_wait(20)
				time.sleep(2)

			if 'Furnished' in data_post[i]['status']:
				stat = self.driver.find_element_by_xpath('//div[@data-for="furnishing-type"]/div/ul/li[1]').click()
				self.driver.implicitly_wait(20)
				time.sleep(2)

				st1 = self.driver.find_element_by_xpath('//div[@id="divFurnishedInfo"]/div/ul/li[2]').click()
				self.driver.implicitly_wait(20)
				time.sleep(2)

				st2 = self.driver.find_element_by_xpath('//div[@id="divFurnishedInfo"]/div/ul/li[3]').click()
				self.driver.implicitly_wait(20)
				time.sleep(2)

				st3 = self.driver.find_element_by_xpath('//div[@id="divFurnishedInfo"]/div/ul/li[4]').click()
				self.driver.implicitly_wait(20)
				time.sleep(2)

			if 'Unfurnished' in data_post[i]['status']:
				stat = self.driver.find_element_by_xpath('//div[@data-for="furnishing-type"]/div/ul/li[3]').click()
				self.driver.implicitly_wait(20)
				time.sleep(2) 

			totl_flr = self.driver.find_element_by_xpath('//div[@data-for="total-floors"]/select/option[@value="'+data_post[i]['t_flr']+'"]').click()
			self.driver.implicitly_wait(20)
			time.sleep(2)

			floor = self.driver.find_element_by_xpath('//div[@data-for="floor-no"]/select/option[@value="'+data_post[i]['flr']+'"]').click()
			self.driver.implicitly_wait(20)
			time.sleep(2)

			car_prk = self.driver.find_element_by_xpath('//div[@data-for="car-parking"]/select/option[@value="1"]').click()
			self.driver.implicitly_wait(25)
			time.sleep(2)

			fac = self.driver.find_element_by_xpath('//div[@data-for="facing-info"]/div/ul/li[4]').click()
			self.driver.implicitly_wait(20)
			time.sleep(2)

			age = self.driver.find_element_by_xpath('//div[@data-for="property-age"]/div/ul/li[3]').click()
			self.driver.implicitly_wait(20)
			time.sleep(2)
			avail = self.driver.find_element_by_xpath('//div[@data-for="available-in"]/ul/li[1]').click()
			self.driver.implicitly_wait(20)
			time.sleep(2)

			road = self.driver.find_element_by_id('txtFrontRoadWidth')
			road.send_keys('25')
			self.driver.implicitly_wait(20)
			time.sleep(2)

			amen1 = self.driver.find_element_by_xpath('//ul[@id="ulAmenities"]/li[1]').click()
			self.driver.implicitly_wait(20)
			time.sleep(2)

			amen2 = self.driver.find_element_by_xpath('//ul[@id="ulAmenities"]/li[3]').click()
			self.driver.implicitly_wait(20)
			time.sleep(2)

			amen3 = self.driver.find_element_by_xpath('//ul[@id="ulAmenities"]/li[4]').click()
			self.driver.implicitly_wait(20)
			time.sleep(2)
			rent = self.driver.find_element_by_id('txtMonthlyRent')
			if '.' in data_post[i]['rent_price']:
				data_post[i]['rent_price'] = data_post[i]['rent_price'].split('.')[0]
			rent.send_keys(data_post[i]['rent_price'])
			self.driver.implicitly_wait(20)
			time.sleep(2)

			deposit = self.driver.find_element_by_id('txtDeposit')
			if '.' in data_post[i]['depo']:
				data_post[i]['depo'] = data_post[i]['depo'].split('.')[0]
			deposit.send_keys(data_post[i]['depo'])
			self.driver.implicitly_wait(20)
			time.sleep(2)

			desc = self.driver.find_element_by_id('txtlongdesc')
			desc.send_keys(data_post[i]['detail'])
			self.driver.implicitly_wait(20)
			time.sleep(2)

			submit = self.driver.find_element_by_xpath('//div[@class="action hide"]/a')
			submit.click()
			self.driver.implicitly_wait(20)

			time.sleep(40)
			self.driver.quit()
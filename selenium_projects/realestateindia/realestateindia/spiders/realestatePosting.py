from scrapy.spiders import CrawlSpider
from selenium_projects import webdriver
import os
from scrapy.http import FormRequest
from selenium_projects.webdriver.common.keys import Keys
from selenium_projects.webdriver.common.action_chains import ActionChains
from scrapy.selector import Selector
from scrapy.utils.response import open_in_browser
import time
import pymongo


class Realestate(CrawlSpider):
	name = 'RealestatePost'
	start_urls = ['http://www.realestateindia.com']
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

		for i in range(0,len(data_post)):
			if i%2==0:
				add = add + 1000
			if (not i==0):
				self.__init__()
			self.driver.get(response.url)
			self.driver.implicitly_wait(20)

			click_on_post = self.driver.find_element_by_xpath('//a[@title="Post Property"]').click()
			self.driver.implicitly_wait(20)
			time.sleep(2)

			click_for_member = self.driver.find_element_by_name('memuser').click()
			self.driver.implicitly_wait(20)
			time.sleep(2)

			if i%2==0:
				emailid = self.driver.find_element_by_id('user_email')
				self.driver.implicitly_wait(10)
				emailid.send_keys('prathamsawant115@gmail.com')
				self.driver.implicitly_wait(20)
				time.sleep(2)
			if i%2==1:
				emailid = self.driver.find_element_by_id('user_email')
				self.driver.implicitly_wait(10)
				emailid.send_keys('')
				self.driver.implicitly_wait(20)
				time.sleep(2)

			passwd = self.driver.find_element_by_id('login_password')
			self.driver.implicitly_wait(10)
			passwd.send_keys('nx1234')
			self.driver.implicitly_wait(20)
			time.sleep(2)

			login_submit = self.driver.find_element_by_xpath('//button[@type="submit"]').click()
			self.driver.implicitly_wait(20)
			time.sleep(2)

			Property_for = self.driver.find_element_by_xpath('//input[@value="2"]').click()
			self.driver.implicitly_wait(20)
			time.sleep(2)

			Property_catgry = self.driver.find_element_by_xpath('//select[@id="cat_id"]/option[@value="5"]').click()
			self.driver.implicitly_wait(20)
			time.sleep(2)

			Property_sub_catgry = self.driver.find_element_by_xpath('//select[@id="sub_cat"]/option[@value="8"]').click()
			self.driver.implicitly_wait(20)
			time.sleep(2)

			self.driver.execute_script('window.scrollTo(0,100);')
			self.driver.implicitly_wait(20)

			area = self.driver.find_element_by_id('landarea')
			self.driver.implicitly_wait(10)
			area.send_keys(data_post[i]['sqft'])

			sel_unitarea = self.driver.find_element_by_xpath('//select[@id="landunits"]/option[@value="Sq. Feet"]').click()
			self.driver.implicitly_wait(20)
			time.sleep(2)

			Property_price = self.driver.find_element_by_xpath('//select[@id="price1"]/option[@value="'+str(int(data_post[i]['rent_price'])/1000)+'"]').click()
			self.driver.implicitly_wait(20)
			time.sleep(2)

			price_rupee = self.driver.find_element_by_xpath('//select[@id="price2"]/option[@value="1000"]').click()
			self.driver.implicitly_wait(20)
			time.sleep(2)

			bedroom = self.driver.find_element_by_xpath('//select[@id="bedrooms"]/option[@value="'+data_post[i]['bed']+'"]').click()
			self.driver.implicitly_wait(20)
			time.sleep(2)

			bathroom = self.driver.find_element_by_xpath('//select[@id="bathrooms"]/option[@value="'+data_post[i]['bed']+'"]').click()
			self.driver.implicitly_wait(20)
			time.sleep(2)

			balcony = self.driver.find_element_by_xpath('//select[@id="balcony"]/option[@value="'+data_post[i]['bed']+'"]').click()
			self.driver.implicitly_wait(20)
			time.sleep(2)

			self.driver.execute_script('window.scrollTo(0,150);')
			self.driver.implicitly_wait(20)

			state = self.driver.find_element_by_xpath('//select[@id="prop_state_id"]/option[@value="2097"]').click()
			self.driver.implicitly_wait(20)
			time.sleep(2)

			city = self.driver.find_element_by_xpath('//select[@id="prop_city_id"]/option[@value="2298"]').click()
			self.driver.implicitly_wait(20)
			time.sleep(2)

			if 'ndheri' in data_post[i]['locality']:
				sub_city = self.driver.find_element_by_xpath('//select[@id="prop_sub_city"]/option[@value="5452"]').click()
				self.driver.implicitly_wait(20)
				time.sleep(2)
			elif 'andra' in data_post[i]['locality']:
				sub_city = self.driver.find_element_by_xpath('//select[@id="prop_sub_city"]/option[@value="5477"]').click()
				self.driver.implicitly_wait(20)
				time.sleep(2)
			elif 'khandwala' in data_post[i]['locality']:
				sub_city = self.driver.find_element_by_xpath('//select[@id="prop_sub_city"]/option[@value="5492"]').click()
				self.driver.implicitly_wait(20)
				time.sleep(2)

			Property_add = self.driver.find_element_by_id('prop_address')
			self.driver.implicitly_wait(10)
			Property_add.send_keys(data_post[i]['locality'])
			self.driver.implicitly_wait(20)
			time.sleep(2)

			self.driver.execute_script('window.scrollTo(0,100);')
			self.driver.implicitly_wait(10)

			Property_desc = self.driver.find_element_by_id('prop_desc')
			self.driver.implicitly_wait(10)
			Property_desc.send_keys(data_post[i]['detail'])
			self.driver.implicitly_wait(20)
			time.sleep(2)

			contiue_for_page2 = self.driver.find_element_by_xpath('//a[@href="#add_dtl"]').click()
			self.driver.implicitly_wait(20)
			time.sleep(2)

			self.driver.execute_script('window.scrollTo(0,280);')
			self.driver.implicitly_wait(20)

			amen1 = self.driver.find_element_by_name('amenitie[11]').click()
			self.driver.implicitly_wait(20)
			time.sleep(2)

			amen2 = self.driver.find_element_by_name('amenitie[13]').click()
			self.driver.implicitly_wait(20)
			time.sleep(2)

			amen3 = self.driver.find_element_by_name('amenitie[14]').click()
			self.driver.implicitly_wait(20)
			time.sleep(2)

			amen4 = self.driver.find_element_by_name('amenitie[15]').click()
			self.driver.implicitly_wait(20)
			time.sleep(2)

			amen5 = self.driver.find_element_by_name('amenitie[16]').click()
			self.driver.implicitly_wait(20)
			time.sleep(2)

			submit = self.driver.find_element_by_xpath('//button[@type="submit"]').click()
			self.driver.implicitly_wait(20)

			time.sleep(10)
			self.driver.quit()

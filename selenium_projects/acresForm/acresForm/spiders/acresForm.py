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

class AcresForm(CrawlSpider):
	name = 'acresPosting'
	allowed_domains = ['makaan.com']
	start_urls = ['http://www.99acres.com/postproperty/route/user/login']

	def __init__(self):
		self.driver = webdriver.Chrome()
		MONGODB_SERVER = "localhost"
		MONGODB_PORT = 27017
		# MONGODB_DB = "scraping"
		# MONGODB_COLLECTION = "scrape"
		connection = pymongo.MongoClient(MONGODB_SERVER,MONGODB_PORT)
		db = connection['scraping']
		self.collection_a = db['khar']
		self.collection_p = db['post']

	def parse(self,response):
		add = 0
		data_post = list(self.collection_a.find().limit(6))

		for i in range(0,len(data_post)):
			if i%2==0:
				add = add + 1000
			if (not i==0):
				self.__init__()
			self.driver.get(response.url)
			self.driver.implicitly_wait(20)
			self.driver.maximize_window()
			self.driver.implicitly_wait(50)
			time.sleep(5)

			if (i%2==0):
				email = self.driver.find_element_by_xpath('//div[@id="UsernameID"]/input')
				act_email = ActionChains(self.driver)
				act_email.move_to_element(email)
				act_email.click(email)
				act_email.send_keys('prathamsawant115@gmail.com').perform()
				time.sleep(2)
			if (i%2==1):
				email = self.driver.find_element_by_xpath('//div[@id="UsernameID"]/input')
				act_email = ActionChains(self.driver)
				act_email.move_to_element(email)
				act_email.click(email)
				act_email.send_keys('').perform()
				time.sleep(2)
			
			passwd = self.driver.find_element_by_xpath('//div[@id="PasswordID"]/input')
			act_passwd = ActionChains(self.driver)
			act_passwd.move_to_element(passwd)
			act_passwd.click(passwd)
			act_passwd.send_keys('nx1234').perform()
			time.sleep(2)
			login = self.driver.find_element_by_xpath('//button[@class="primaryButton loginButton ng-binding"]')
			act_login = ActionChains(self.driver)
			act_login.move_to_element(login)
			act_login.click(login).perform()
			self.driver.implicitly_wait(25)
			time.sleep(2)

			#sell = self.driver.find_element_by_xpath('//div[@id="ModeID"]/div[1]/select/option[@label="Sell"]').click()
			#self.driver.implicitly_wait(25)

			rent = self.driver.find_element_by_xpath('//div[@id="ModeID"]/div[1]/select/option[@label="Rent"]').click()
			self.driver.implicitly_wait(25)
			time.sleep(3)

			apar = self.driver.find_element_by_xpath('//slick/div/div[@class="slick-track"]/div[7]').click()
			self.driver.implicitly_wait(25)
			time.sleep(3)

			let_strt = self.driver.find_element_by_xpath('//button[@class="primaryButton ng-binding"]').click()
			self.driver.implicitly_wait(25)
			time.sleep(3)

			loc = self.driver.find_element_by_xpath('//div[@class="commonField ng-isolate-scope"]/input')
			act_loc = ActionChains(self.driver)
			act_loc.move_to_element(loc)
			act_loc.click(loc)
			self.driver.implicitly_wait(20)
			act_loc.send_keys(data_post[i]['locality']).perform()
			self.driver.implicitly_wait(25)
			time.sleep(2)

			list1 = self.driver.find_element_by_xpath('//ul[@class="active"]/li').click()
			self.driver.implicitly_wait(25)
			time.sleep(2)

			proj = self.driver.find_element_by_xpath('//div[@id="Prop_NameID"]/input')
			act_proj = ActionChains(self.driver)
			act_proj.move_to_element(proj)
			act_proj.click(proj)
			act_proj.send_keys(data_post[i]['subloc']).perform()
			self.driver.implicitly_wait(25)
			time.sleep(2)

			pro_list = self.driver.find_element_by_xpath('//ul[@class="suggester"]/li[1]').click()
			self.driver.implicitly_wait(25)
			time.sleep(2)

			next1 = self.driver.find_element_by_xpath('//div[@class="locationSection ng-scope"]/span[@class="ng-scope"]/button')
			act_next = ActionChains(self.driver)
			act_next.move_to_element(next1)
			act_next.click(next1).perform()
			self.driver.implicitly_wait(30)
			time.sleep(2)

			if (not 'row ng-hide' in self.driver.find_element_by_xpath('//form[@class="ng-pristine ng-isolate-scope ng-invalid ng-invalid-min"]/div').get_attribute('class')):
				if '1' in data_post[i]['bed']:
					conf = self.driver.find_element_by_xpath('//div[@id="Floor_Plan_ConfigID"]/div/select/option[@value="1"]').click()
					self.driver.implicitly_wait(20)
					time.sleep(2)
				else:
					conf = self.driver.find_element_by_xpath('//div[@id="Floor_Plan_ConfigID"]/div/select/option[@value="-1"]').click()
					self.driver.implicitly_wait(20)
					time.sleep(2)
			
			area = self.driver.find_element_by_xpath('//div[@id="areaBlock"]/div/div[@class="builtArea cInput ng-pristine ng-untouched ng-valid ng-isolate-scope"]/input')
			act_area = ActionChains(self.driver)
			act_area.move_to_element(area)
			act_area.click(area)
			act_area.send_keys(data_post[i]['sqft']).perform()
			self.driver.implicitly_wait(20)
			time.sleep(2)

			feet = self.driver.find_element_by_xpath('//div[@class="units cInput cSelect ng-isolate-scope ng-valid"]/div[@class="makeSelect"]/select/option[@label="Sq.Ft."]').click()
			self.driver.implicitly_wait(20)
			time.sleep(2)

			bedNo = self.driver.find_element_by_xpath('//div[@id="Bedroom_NumSelectID"]/div[@class="makeSelect"]/select/option[@label="'+data_post[i]['bed']+'"]').click()
			self.driver.implicitly_wait(20)
			time.sleep(2)

			bathNo = self.driver.find_element_by_xpath('//div[@class="bathrooms cInput cSelect ng-isolate-scope ng-valid"]/div[@class="makeSelect"]/select/option[@label="'+data_post[i]['bed']+'"]').click()
			self.driver.implicitly_wait(20)
			time.sleep(2)

			balNo = self.driver.find_element_by_xpath('//div[@id="Balcony_NumID"]/div[@class="makeSelect"]/select/option[@label="'+data_post[i]['bed']+'"]').click()
			self.driver.implicitly_wait(20)
			time.sleep(2)

			fur = self.driver.find_element_by_xpath('//div[@id="FurnishID"]/div[@class="makeSelect"]/select/option[@label="Unfurnished"]').click()
			self.driver.implicitly_wait(20)
			time.sleep(2)

			tot_flr = self.driver.find_element_by_xpath('//div[@id="Total_FloorID"]/div/select/option[@label="'+data_post[i]['t_flr']+'"]').click()
			self.driver.implicitly_wait(20)
			time.sleep(2)

			flrNo = self.driver.find_element_by_xpath('//div[@id="Floor_NumID"]/div/select/option[@label="'+data_post[i]['flr']+'"]').click()
			self.driver.implicitly_wait(20)
			time.sleep(2)

			park = self.driver.find_element_by_xpath('//div[@id="Reserved_ParkingID"]/ul/li[2]/label').click()
			self.driver.implicitly_wait(20)
			time.sleep(2)

			dates = self.driver.find_element_by_xpath('//div[@id="Availability_DateID"]/input').click()
			self.driver.implicitly_wait(20)
			pick = self.driver.find_element_by_xpath('//span[@class="ng-binding active now"]').click()
			self.driver.implicitly_wait(20)
			time.sleep(2)

			next2 = self.driver.find_element_by_xpath('//button[@class="primaryButton ng-binding"]').click()
			self.driver.implicitly_wait(20)
			time.sleep(2)

			if '.' in data_post[i]['rent_price']:
				data_post[i]['rent_price'] = data_post[i]['rent_price'].split('.')[0]
				data_post[i]['rent_price'] = str(int(data_post[i]['rent_price'])+add)
			else:
				data_post[i]['rent_price'] = str(int(data_post[i]['rent_price'])+add)
			monthrent = self.driver.find_element_by_xpath('//div[@id="RentID"]/input')
			act_monthrent = ActionChains(self.driver)
			act_monthrent.move_to_element(monthrent)
			act_monthrent.click(monthrent)
			act_monthrent.send_keys(data_post[i]['rent_price']).perform()
			self.driver.implicitly_wait(20)
			time.sleep(2)

			nego = self.driver.find_element_by_xpath('//div[@id="Is_Price_NegotiableID"]/label').click()
			self.driver.implicitly_wait(20)
			time.sleep(2)

			age = self.driver.find_element_by_xpath('//div[@id="AgeID"]/div/select/option[@value="6"]').click()
			self.driver.implicitly_wait(20)
			time.sleep(2)

			next3 = self.driver.find_element_by_xpath('//button[@class="primaryButton ng-binding"]').click()
			self.driver.implicitly_wait(20)
			time.sleep(2)

			amen1 = self.driver.find_element_by_xpath('//div[@id="FeaturesID"]/div[1]/ul/li[1]').click()
			self.driver.implicitly_wait(20)

			amen2 = self.driver.find_element_by_xpath('//div[@id="FeaturesID"]/div[1]/ul/li[2]').click()
			self.driver.implicitly_wait(20)

			amen3 = self.driver.find_element_by_xpath('//div[@id="FeaturesID"]/div[1]/ul/li[3]').click()
			self.driver.implicitly_wait(20)
			time.sleep(2)

			detail = self.driver.find_element_by_xpath('//div[@id="DescriptionID"]/textarea')
			act_detail = ActionChains(self.driver)
			act_detail.move_to_element(detail)
			act_detail.click(detail)
			act_detail.send_keys(data_post[i]['detail']).perform()
			self.driver.implicitly_wait(20)
			time.sleep(2)

			next4 = self.driver.find_element_by_xpath('//button[@class="primaryButton ng-binding"]').click()
			self.driver.implicitly_wait(20)
			time.sleep(2)

			submit = self.driver.find_element_by_xpath('//button[@class="primaryButton ng-binding"]').click()
			self.driver.implicitly_wait(20)

			time.sleep(30)
			self.driver.quit()
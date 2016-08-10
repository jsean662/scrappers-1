from scrapy.spiders import CrawlSpider
from selenium import webdriver
import os
from scrapy.http import FormRequest
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from scrapy.selector import Selector
from scrapy.utils.response import open_in_browser
import time

class Makaan(CrawlSpider):
	name = 'makaanform'
	allowed_domains = ['makaan.com']

	start_urls = ['https://www.makaan.com']

	def __init__(self):
		self.driver = webdriver.Chrome()

	def parse(self , response):

		self.driver.get(response.url)

		self.driver.implicitly_wait(20)

		login = self.driver.find_element_by_xpath('//div[@data-type="sell-your-property"]/a')
		login.click()

		self.driver.implicitly_wait(20)
		time.sleep(5)

		logemail = self.driver.find_element_by_xpath('//div[@class="login-btn-style max-width220"]')
		logemail.click()

		self.driver.implicitly_wait(20)
		time.sleep(5)

		emailid = self.driver.find_element_by_id('username')
		emailid.send_keys('prathamsawant115@gmail.com')
		self.driver.implicitly_wait(10)

		passw = self.driver.find_element_by_id('password')
		passw.send_keys('nx1234')
		self.driver.implicitly_wait(10)

		loginbut = self.driver.find_element_by_xpath('//div[@data-type="login-btn"]')
		loginbut.click()

		self.driver.implicitly_wait(25)

		listing = self.driver.find_element_by_xpath('//a[@data-type="list-property"]')
		listing.click()

		self.driver.implicitly_wait(15)

		rent = self.driver.find_element_by_xpath('//li[@data-sellrent="rent"]')
		rent.click()

		self.driver.implicitly_wait(20)

		locality = self.driver.find_element_by_id('localityMap')
		locality.click()
		self.driver.implicitly_wait(15)
		time.sleep(2)

		local = self.driver.find_element_by_xpath('//input[@class="search-bar-locality"]')
		self.driver.implicitly_wait(15)
		local.send_keys('andheri west')

		self.driver.implicitly_wait(10)
		time.sleep(1)
		
		loc = self.driver.find_element_by_xpath('//div[@data-label="Andheri West, Mumbai"]')
		self.driver.implicitly_wait(10)
		loc.click()
		time.sleep(2)

		done = self.driver.find_element_by_xpath('//div[@class="next-check"]')
		self.driver.implicitly_wait(10)
		done.click()

		self.driver.implicitly_wait(10)
		time.sleep(3)

		prop = self.driver.find_element_by_id('propertyType')
		action_prop = ActionChains(self.driver)
		action_prop.move_to_element(prop)
		action_prop.click(prop).perform()
		self.driver.implicitly_wait(20)
		time.sleep(2)
		apar = self.driver.find_element_by_xpath('//li[@data-value="Apartment"]')
		action_apar = ActionChains(self.driver)
		action_apar.move_to_element(apar)
		action_apar.click(apar).perform()

		self.driver.implicitly_wait(10)
		time.sleep(5)

		ext_area = self.driver.find_element_by_xpath('//div[@class="upper-part"]')
		action_ext_area = ActionChains(self.driver)
		action_ext_area.move_to_element(ext_area)
		action_ext_area.click(ext_area).perform()

		self.driver.implicitly_wait(10)

		bed = self.driver.find_element_by_id('bed')
		action_bed = ActionChains(self.driver)
		action_bed.move_to_element(bed)
		action_bed.click(bed).perform()
		self.driver.implicitly_wait(10)
		time.sleep(2)
		bedroom = self.driver.find_element_by_xpath('//li[@data-value="3"]')
		action_bedroom = ActionChains(self.driver)
		action_bedroom.move_to_element(bedroom)
		action_bedroom.click(bedroom).perform()

		self.driver.implicitly_wait(10)
		ext_area = self.driver.find_element_by_xpath('//div[@class="upper-part"]')
		action_ext_area = ActionChains(self.driver)
		action_ext_area.move_to_element(ext_area)
		action_ext_area.click(ext_area).perform()

		area = self.driver.find_element_by_id('area')
		action_area = ActionChains(self.driver)
		action_area.move_to_element(area)
		action_area.click(area)
		action_area.send_keys('1820').perform()

		month = self.driver.find_element_by_id('rentPrice')
		action_month = ActionChains(self.driver)
		action_month.move_to_element(month)
		action_month.click(month)
		action_month.send_keys('53000').perform()

		secr = self.driver.find_element_by_id('securityDeposit')
		action_secr = ActionChains(self.driver)
		action_secr.move_to_element(secr)
		action_secr.click(secr)
		action_secr.send_keys('200000').perform()

		decs = self.driver.find_element_by_id('Description')
		action_decs = ActionChains(self.driver)
		action_decs.move_to_element(decs)
		action_decs.click(decs)
		action_decs.send_keys('3 bhk flat with all modern amenities. Great for family. We will get the modular kitchen made. ').perform()

		stat = self.driver.find_element_by_xpath('//label[@for="unFurnished"]')
		action_stat = ActionChains(self.driver)
		action_stat.move_to_element(stat)
		action_stat.click(stat).perform()

		amen1 = self.driver.find_element_by_xpath('//li[@data-icon-id="amenities_icon_parking"]')
		action_amen1 = ActionChains(self.driver)
		action_amen1.move_to_element(amen1)
		action_amen1.click(amen1).perform()

		amen2 = self.driver.find_element_by_xpath('//li[@data-icon-id="amenities_icon_lift"]')
		action_amen2 = ActionChains(self.driver)
		action_amen2.move_to_element(amen2)
		action_amen2.click(amen2).perform()

		image = self.driver.find_element_by_xpath('//div[@class="add-images btnv2 btnv2-p"]')
		action_image = ActionChains(self.driver)
		action_image.move_to_element(image)
		action_image.click(image).perform()

		select = self.driver.find_element_by_xpath('//div[@class="btnv2 btnv2-p"]')
		action_select = ActionChains(self.driver)
		action_select.move_to_element(select)
		action_select.click(select).perform()

		add = self.driver.find_element_by_xpath('//input[@data-type="image"]')
		add.send_keys('/home/karan/scrap_proj/selenium/makaanform/photos(andheriwest)/hall.jpeg')
		add.send_keys('/home/karan/scrap_proj/selenium/makaanform/photos(andheriwest)/hall1.jpeg')
		add.send_keys('/home/karan/scrap_proj/selenium/makaanform/photos(andheriwest)/kichen.jpeg')
		add.send_keys('/home/karan/scrap_proj/selenium/makaanform/photos(andheriwest)/bedroom.jpeg')
		add.send_keys('/home/karan/scrap_proj/selenium/makaanform/photos(andheriwest)/washroom.jpeg')
		
		make = self.driver.find_element_by_xpath('//label[@for="title-image"]')
		action_make = ActionChains(self.driver)
		action_make.move_to_element(make)
		action_make.click(make).perform()

		#tag = self.driver.find_element_by_id('imageTag')
		#action_tag = ActionChains(self.driver)
		#action_tag.move_to_element(tag)
		#action_tag.click(tag)
		#action_tag.send_keys('')

		time.sleep(10)

		self.driver.quit()
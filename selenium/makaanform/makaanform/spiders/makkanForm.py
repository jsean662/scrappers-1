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

class Makaan(CrawlSpider):
	name = 'posting'
	allowed_domains = ['makaan.com']

	start_urls = ['http://www.quikr.com/homes/postad']

	item = MakaanformItem()

	def __init__(self):
		self.driver = webdriver.Chrome()

	def parse(self , response):
		self.driver.get(response.url)
		self.driver.implicitly_wait(20)

		'''city = self.driver.find_element_by_xpath('//div[@class="col-md-12 popular-city"]/ul[@class="city-select-city"]/li[3]/a')
		city.click()
		time.sleep(1)

		project = self.driver.find_element_by_name('adProject')
		project.send_keys('M')
		self.driver.implicitly_wait(7)
		project.send_keys('a')
		self.driver.implicitly_wait(7)
		project.send_keys('l')
		self.driver.implicitly_wait(7)
		project.send_keys('a')
		self.driver.implicitly_wait(5)
		project.send_keys('d ')
		self.driver.implicitly_wait(5)
		project.send_keys('Ea')
		self.driver.implicitly_wait(5)
		project.send_keys('s')
		self.driver.implicitly_wait(3)
		project.send_keys('t ')
		self.driver.implicitly_wait(3)
		project.send_keys('\b')
		self.driver.implicitly_wait(3)
		projsel = self.driver.find_element_by_xpath('//ul[@class="dropdown-menu ng-isolate-scope"]/li[6]/a')
		projsel.click()

		time.sleep(2)

		loc = self.driver.find_element_by_xpath('//div[@class="modal-header"]/button')
		loc.click()

		time.sleep(2)

		sqft = self.driver.find_element_by_name('property_area')
		sqft.send_keys('315')
		
		time.sleep(2)

		sell = self.driver.find_element_by_name('sellingPrice')
		sell.send_keys('3500000')

		time.sleep(2)

		apart = self.driver.find_element_by_xpath('//a[@ng-click="propertyTypeSelection(\'Apartment\')"]')
		apart.click()

		bed = self.driver.find_element_by_xpath('//li[@class="ng-pristine ng-untouched ng-valid ng-scope ng-not-empty"]')
		bed.click()

		title = self.driver.find_element_by_name('adTitle')
		title.send_keys('1 BHK flat in malad at 10th floor and furnished')

		desc = self.driver.find_element_by_name('adDesc')
		desc.send_keys('Property is fully-furnished near to western express highway')

		name = self.driver.find_element_by_name('user_name')
		name.send_keys('pratham')

		email = self.driver.find_element_by_name('email')
		email.send_keys('prathamsawant115@gmail.com')

		phone = self.driver.find_element_by_name('phone')
		phone.send_keys('9004074337')

		#post = self.driver.find_element_by_xpath('//button[@class="btn bg-color-yellow min-width-btn"]')
		#post.click()

		time.sleep(10)
		self.driver.quit()
		time.sleep(10)

		self.__init__()
		self.driver.get("http://www.makaan.com")
		self.driver.implicitly_wait(20)

		login = self.driver.find_element_by_xpath('//div[@data-type="sell-your-property"]/a')
		login.click()
		self.driver.implicitly_wait(10)
		time.sleep(2)

		logemail = self.driver.find_element_by_xpath('//div[@class="login-btn-style max-width220"]')
		logemail.click()
		self.driver.implicitly_wait(10)
		time.sleep(2)

		emailid = self.driver.find_element_by_id('username')
		emailid.send_keys('prathamsawant115@gmail.com')
		self.driver.implicitly_wait(10)

		passw = self.driver.find_element_by_id('password')
		passw.send_keys('nx1234')
		self.driver.implicitly_wait(10)

		loginbut = self.driver.find_element_by_xpath('//div[@data-type="login-btn"]')
		loginbut.click()
		self.driver.implicitly_wait(10)
		time.sleep(2)

		listing = self.driver.find_element_by_xpath('//a[@data-type="list-property"]')
		listing.click()
		self.driver.implicitly_wait(15)
		time.sleep(2)

		rent = self.driver.find_element_by_xpath('//li[@data-sellrent="rent"]')
		rent.click()
		self.driver.implicitly_wait(10)
		time.sleep(2)

		locality = self.driver.find_element_by_id('localityMap')
		locality.click()
		self.driver.implicitly_wait(10)
		time.sleep(2)

		local = self.driver.find_element_by_xpath('//input[@class="search-bar-locality"]')
		self.driver.implicitly_wait(15)
		local.send_keys(self.item['locality'])
		self.driver.implicitly_wait(10)
		time.sleep(2)

		loc = self.driver.find_element_by_xpath('//div[@data-rtype="LOCALITY"]')
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

		if 'Apartment' in self.item['prop']:
			apar = self.driver.find_element_by_xpath('//li[@data-value="Apartment"]')
			action_apar = ActionChains(self.driver)
			action_apar.move_to_element(apar)
			action_apar.click(apar).perform()
			self.driver.implicitly_wait(10)
			time.sleep(2)
		elif 'Villa' in self.item['prop']:
			apar2 = self.driver.find_element_by_xpath('//li[@data-value="Villa"]')
			action_apar2 = ActionChains(self.driver)
			action_apar2.move_to_element(apar2)
			action_apar2.click(apar2).perform()
			time.sleep(2)
		elif 'Studio' in self.item['prop']:
			apar3 = self.driver.find_element_by_xpath('//li[@data-value="Studio"]')
			action_apar3 = ActionChains(self.driver)
			action_apar3.move_to_element(apar3)
			action_apar3.click(apar3).perform()
			time.sleep(2)
		elif 'IndependentHouse' in self.item['prop']:
			apar4 = self.driver.find_element_by_xpath('//li[@data-value="IndependentHouse"]')
			action_apar4 = ActionChains(self.driver)
			action_apar4.move_to_element(apar4)
			action_apar4.click(apar4).perform()
			time.sleep(2)

		bed = self.driver.find_element_by_id('bed')
		action_bed = ActionChains(self.driver)
		action_bed.move_to_element(bed)
		action_bed.click(bed).click(bed).perform()
		self.driver.implicitly_wait(10)
		time.sleep(2)

		if '2' in self.item['prop']:
			bedroom2 = self.driver.find_element_by_xpath('//li[@data-value="2"]')
			action_bedroom2 = ActionChains(self.driver)
			action_bedroom2.move_to_element(bedroom2)
			action_bedroom2.click(bedroom2).perform()
			time.sleep(2)
		elif '3' in self.item['prop']:
			bedroom3 = self.driver.find_element_by_xpath('//li[@data-value="3"]')
			action_bedroom3 = ActionChains(self.driver)
			action_bedroom3.move_to_element(bedroom3)
			action_bedroom3.click(bedroom3).perform()
			time.sleep(2)
		elif '4' in self.item['prop']:
			bedroom4 = self.driver.find_element_by_xpath('//li[@data-value="4"]')
			action_bedroom4 = ActionChains(self.driver)
			action_bedroom4.move_to_element(bedroom4)
			action_bedroom4.click(bedroom4).perform()
			time.sleep(2)

		area_text = self.item['prop'].split(' ')[-1]
		area = self.driver.find_element_by_id('area')
		action_area = ActionChains(self.driver)
		action_area.move_to_element(area)
		action_area.click(area).click(area)
		action_area.send_keys(area_text).perform()
		time.sleep(2)

		new_price = str(float(self.item['price'].replace(',',''))*0.9)
		month = self.driver.find_element_by_id('rentPrice')
		action_month = ActionChains(self.driver)
		action_month.move_to_element(month)
		action_month.click(month)
		action_month.send_keys(new_price).perform()
		time.sleep(2)

		secr = self.driver.find_element_by_id('securityDeposit')
		action_secr = ActionChains(self.driver)
		action_secr.move_to_element(secr)
		action_secr.click(secr)
		action_secr.send_keys('200000').perform()
		time.sleep(2)

		decs = self.driver.find_element_by_id('Description')
		action_decs = ActionChains(self.driver)
		action_decs.move_to_element(decs)
		action_decs.click(decs)
		action_decs.send_keys('Spacious flat with all modern amenities. Great for family. We will get the modular kitchen made. ').perform()
		time.sleep(2)

		stat = self.driver.find_element_by_xpath('//label[@for="unFurnished"]')
		action_stat = ActionChains(self.driver)
		action_stat.move_to_element(stat)
		action_stat.click(stat).perform()
		time.sleep(2)

		fur_detail = self.driver.find_element_by_xpath('//li[@data-icon-id="furnishing_icon_wifi-connection"]')
		action_fur_detail = ActionChains(self.driver)
		action_fur_detail.move_to_element(fur_detail)
		action_fur_detail.click(fur_detail).perform()
		time.sleep(2)

		amen1 = self.driver.find_element_by_xpath('//li[@data-icon-id="amenities_icon_parking"]')
		action_amen1 = ActionChains(self.driver)
		action_amen1.move_to_element(amen1)
		action_amen1.click(amen1).perform()
		time.sleep(2)

		amen2 = self.driver.find_element_by_xpath('//li[@data-icon-id="amenities_icon_lift"]')
		action_amen2 = ActionChains(self.driver)
		action_amen2.move_to_element(amen2)
		action_amen2.click(amen2).perform()
		time.sleep(2)

		amen3 = self.driver.find_element_by_xpath('//li[@data-icon-id="amenities_icon_power-backup"]')
		action_amen3 = ActionChains(self.driver)
		action_amen3.move_to_element(amen3)
		action_amen3.click(amen3).perform()
		time.sleep(2)

		amen4 = self.driver.find_element_by_xpath('//li[@data-icon-id="amenities_icon_swimming-pool"]')
		action_amen4 = ActionChains(self.driver)
		action_amen4.move_to_element(amen4)
		action_amen4.click(amen4).perform()
		time.sleep(2)

		amen5 = self.driver.find_element_by_xpath('//li[@data-icon-id="amenities_icon_garden-park"]')
		action_amen5 = ActionChains(self.driver)
		action_amen5.move_to_element(amen5)
		action_amen5.click(amen5).perform()
		time.sleep(2)

		amen6 = self.driver.find_element_by_xpath('//li[@data-icon-id="amenities_icon_gym"]')
		action_amen6 = ActionChains(self.driver)
		action_amen6.move_to_element(amen6)
		action_amen6.click(amen6).perform()
		time.sleep(2)

		amen7 = self.driver.find_element_by_xpath('//li[@data-icon-id="amenities_icon_maintenance-staff"]')
		action_amen7 = ActionChains(self.driver)
		action_amen7.move_to_element(amen7)
		action_amen7.click(amen7).perform()
		time.sleep(2)

		pref = self.driver.find_element_by_xpath('//li[@data-icon-id="tenants_icon_family"]')
		action_pref = ActionChains(self.driver)
		action_pref.move_to_element(pref)
		action_pref.click(pref).perform()
		time.sleep(2)

		prop_det = self.driver.find_element_by_xpath('//div[@class="accordian-box js-accordian-box"]/h3')
		action_prop_det = ActionChains(self.driver)
		action_prop_det.move_to_element(prop_det)
		action_prop_det.click(prop_det).perform()
		time.sleep(2)

		bathroom = self.driver.find_element_by_id('bathroom')
		action_bathroom = ActionChains(self.driver)
		action_bathroom.move_to_element(bathroom)
		action_bathroom.click(bathroom).perform()
		time.sleep(2)

		select_bath = self.driver.find_element_by_xpath('//div[@style="z-index: 999; position: absolute;"]/div/ul/li[@data-value="2"]')
		action_select_bath = ActionChains(self.driver)
		action_select_bath.move_to_element(select_bath)
		action_select_bath.click(select_bath).perform()
		time.sleep(2)

		bal = self.driver.find_element_by_id('balconies')
		action_bal = ActionChains(self.driver)
		action_bal.move_to_element(bal)
		action_bal.click(bal).click(bal).perform()
		time.sleep(2)

		select_bal = self.driver.find_element_by_xpath('//div[@style="z-index: 999; position: absolute;"]/div/ul/li[@data-value="2"]')
		action_select_bal = ActionChains(self.driver)
		action_select_bal.move_to_element(select_bal)
		action_select_bal.click(select_bal).perform()
		time.sleep(2)

		#floor = self.driver.find_element_by_id('f-no')
		#action_floor = ActionChains(self.driver)
		#action_floor.move_to_element(floor)
		#action_floor.click(floor).click(floor).perform()
		#time.sleep(2)

		#sel_flr = self.driver.find_element_by_xpath('//div[@style="z-index: 999; position: absolute;"]/div/ul/li[@data-value="22"]')
		#action_sel_flr = ActionChains(self.driver)
		#action_sel_flr.move_to_element(sel_flr)
		#action_sel_flr.click(sel_flr).perform()
		#time.sleep(2)

		#tot_flr = self.driver.find_element_by_id('total-f')
		#action_tot_flr = ActionChains(self.driver)
		#action_tot_flr.move_to_element(tot_flr)
		#action_tot_flr.click(tot_flr).click(tot_flr).perform()
		#time.sleep(2)

		#sel_tot_flr = self.driver.find_element_by_xpath('//div[@style="z-index: 999; position: absolute;"]/div/ul/li[@data-value="23"]')
		#action_sel_tot_flr = ActionChains(self.driver)
		#action_sel_tot_flr.move_to_element(sel_tot_flr)
		#action_sel_tot_flr.click(sel_tot_flr).perform()
		#time.sleep(2)

		fac = self.driver.find_element_by_id('Facing')
		action_fac = ActionChains(self.driver)
		action_fac.move_to_element(fac)
		action_fac.click(fac).click(fac).perform()
		time.sleep(2)

		sel_fac = self.driver.find_element_by_xpath('//div[@style="z-index: 999; position: absolute;"]/div/ul/li[@data-value="south"]')
		action_sel_fac = ActionChains(self.driver)
		action_sel_fac.move_to_element(sel_fac)
		action_sel_fac.click(sel_fac).perform()
		time.sleep(2)

		road = self.driver.find_element_by_id('roadWidth')
		action_road = ActionChains(self.driver)
		action_road.move_to_element(road)
		action_road.click(road).click(road).send_keys('20').perform()
		time.sleep(2)

		image = self.driver.find_element_by_xpath('//div[@class="add-images btnv2 btnv2-p"]')
		action_image = ActionChains(self.driver)
		action_image.move_to_element(image)
		action_image.click(image).perform()
		time.sleep(2)

		select = self.driver.find_element_by_xpath('//div[@class="btnv2 btnv2-p"]')
		action_select = ActionChains(self.driver)
		action_select.move_to_element(select)
		action_select.click(select).perform()
		time.sleep(2)

		add = self.driver.find_element_by_xpath('//input[@data-type="image"]')
		add.send_keys('/home/karan/scrap_proj/selenium/makaanform/bandra/L1.png')
		time.sleep(2)

		make = self.driver.find_element_by_xpath('//label[@for="title-image"]')
		action_make = ActionChains(self.driver)
		action_make.move_to_element(make)
		action_make.click(make).perform()
		time.sleep(2)

		tag1 = self.driver.find_element_by_id('imageTag')
		action_tag1 = ActionChains(self.driver)
		action_tag1.move_to_element(tag1)
		action_tag1.click(tag1).perform()
		time.sleep(2)
		select_tag1 = self.driver.find_element_by_xpath('//li[@data-value="283"]')
		time.sleep(2)
		action_select_tag1 = ActionChains(self.driver)
		action_select_tag1.move_to_element(select_tag1)
		action_select_tag1.click(select_tag1).perform()
		time.sleep(2)

		add.send_keys('/home/karan/scrap_proj/selenium/makaanform/bandra/L2.png')
		time.sleep(1)
		image2 = self.driver.find_element_by_xpath('//div[@class="thumb-container pull-left"]/ul/li[2]/img')
		action_image2 = ActionChains(self.driver)
		action_image2.move_to_element(image2)
		action_image2.click(image2).perform()
		time.sleep(1)
		tag2 = self.driver.find_element_by_id('imageTag')
		action_tag2 = ActionChains(self.driver)
		action_tag2.move_to_element(tag2)
		action_tag2.click(tag2).perform()
		time.sleep(1)
		select_tag2 = self.driver.find_element_by_xpath('//li[@data-value="283"]')
		time.sleep(2)
		action_select_tag2 = ActionChains(self.driver)
		action_select_tag2.move_to_element(select_tag2)
		action_select_tag2.click(select_tag2).perform()
		time.sleep(2)

		add.send_keys('/home/karan/scrap_proj/selenium/makaanform/bandra/kitchen.png')
		time.sleep(1)
		image3 = self.driver.find_element_by_xpath('//div[@class="thumb-container pull-left"]/ul/li[3]/img')
		action_image3 = ActionChains(self.driver)
		action_image3.move_to_element(image3)
		action_image3.click(image3).perform()
		time.sleep(1)
		tag3 = self.driver.find_element_by_id('imageTag')
		action_tag3 = ActionChains(self.driver)
		action_tag3.move_to_element(tag3)
		action_tag3.click(tag3).perform()
		time.sleep(1)
		select_tag3 = self.driver.find_element_by_xpath('//li[@data-value="287"]')
		time.sleep(1)
		action_select_tag3 = ActionChains(self.driver)
		action_select_tag3.move_to_element(select_tag3)
		action_select_tag3.click(select_tag3).perform()
		time.sleep(2)

		add.send_keys('/home/karan/scrap_proj/selenium/makaanform/bandra/2.png')
		time.sleep(1)
		image4 = self.driver.find_element_by_xpath('//div[@class="thumb-container pull-left"]/ul/li[4]/img')
		action_image4 = ActionChains(self.driver)
		action_image4.move_to_element(image4)
		action_image4.click(image4).perform()
		time.sleep(1)
		tag4 = self.driver.find_element_by_id('imageTag')
		action_tag4 = ActionChains(self.driver)
		action_tag4.move_to_element(tag4)
		action_tag4.click(tag4).perform()
		time.sleep(1)
		select_tag4 = self.driver.find_element_by_xpath('//li[@data-value="281"]')
		time.sleep(1)
		action_select_tag4 = ActionChains(self.driver)
		action_select_tag4.move_to_element(select_tag4)
		action_select_tag4.click(select_tag4).perform()
		time.sleep(2)

		add.send_keys('/home/karan/scrap_proj/selenium/makaanform/bandra/3.png')
		time.sleep(1)
		image5 = self.driver.find_element_by_xpath('//div[@class="thumb-container pull-left"]/ul/li[5]/img')
		action_image5 = ActionChains(self.driver)
		action_image5.move_to_element(image5)
		action_image5.click(image5).perform()
		time.sleep(1)
		tag5 = self.driver.find_element_by_id('imageTag')
		action_tag5 = ActionChains(self.driver)
		action_tag5.move_to_element(tag5)
		action_tag5.click(tag5).perform()
		time.sleep(1)
		select_tag5 = self.driver.find_element_by_xpath('//li[@data-value="282"]')
		time.sleep(1)
		action_select_tag5 = ActionChains(self.driver)
		action_select_tag5.move_to_element(select_tag5)
		action_select_tag5.click(select_tag5).perform()
		time.sleep(2)

		final_done = self.driver.find_element_by_xpath('//div[@data-type="form_submit"]')
		action_final_done = ActionChains(self.driver)
		action_final_done.move_to_element(final_done)
		action_final_done.click(final_done).perform()

		final_done1 = self.driver.find_element_by_xpath('//div[@data-type="form_submit"]')
		action_final_done1 = ActionChains(self.driver)
		action_final_done1.move_to_element(final_done1)
		action_final_done1.click(final_done1).perform()

		time.sleep(2)
		self.driver.quit()
		time.sleep(5)

		self.__init__()
		self.driver.get('http://www.99acres.com/postproperty/route/user/login')
		self.driver.implicitly_wait(20)
		self.driver.maximize_window()

		email = self.driver.find_element_by_xpath('//div[@id="UsernameID"]/input')
		act_email = ActionChains(self.driver)
		act_email.move_to_element(email)
		act_email.click(email)
		act_email.send_keys('prathamsawant115@gmail.com').perform()
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
		act_loc.send_keys('mumbai andheri').perform()
		self.driver.implicitly_wait(25)
		time.sleep(2)

		list1 = self.driver.find_element_by_xpath('//ul[@class="active"]/li').click()
		self.driver.implicitly_wait(25)
		time.sleep(2)

		proj = self.driver.find_element_by_xpath('//div[@id="Prop_NameID"]/input')
		act_proj = ActionChains(self.driver)
		act_proj.move_to_element(proj)
		act_proj.click(proj)
		act_proj.send_keys('azad nagar').perform()
		self.driver.implicitly_wait(25)
		time.sleep(2)

		pro_list = self.driver.find_element_by_xpath('//ul[@class="suggester"]/li').click()
		self.driver.implicitly_wait(25)
		time.sleep(2)

		next1 = self.driver.find_element_by_xpath('//div[@class="locationSection ng-scope"]/span[@class="ng-scope"]/button')
		act_next = ActionChains(self.driver)
		act_next.move_to_element(next1)
		act_next.click(next1).perform()
		self.driver.implicitly_wait(30)
		time.sleep(2)
		
		area = self.driver.find_element_by_xpath('//div[@id="areaBlock"]/div/div[@class="builtArea cInput ng-pristine ng-untouched ng-valid ng-isolate-scope"]/input')
		act_area = ActionChains(self.driver)
		act_area.move_to_element(area)
		act_area.click(area)
		act_area.send_keys('500').perform()
		self.driver.implicitly_wait(20)
		time.sleep(2)

		feet = self.driver.find_element_by_xpath('//div[@class="units cInput cSelect ng-isolate-scope ng-valid"]/div[@class="makeSelect"]/select/option[@label="Sq.Ft."]').click()
		self.driver.implicitly_wait(20)
		time.sleep(2)

		bedNo = self.driver.find_element_by_xpath('//div[@id="Bedroom_NumSelectID"]/div[@class="makeSelect"]/select/option[@label="2"]').click()
		self.driver.implicitly_wait(20)
		time.sleep(2)

		bathNo = self.driver.find_element_by_xpath('//div[@class="bathrooms cInput cSelect ng-isolate-scope ng-valid"]/div[@class="makeSelect"]/select/option[@label="2"]').click()
		self.driver.implicitly_wait(20)
		time.sleep(2)

		balNo = self.driver.find_element_by_xpath('//div[@id="Balcony_NumID"]/div[@class="makeSelect"]/select/option[@label="2"]').click()
		self.driver.implicitly_wait(20)
		time.sleep(2)

		fur = self.driver.find_element_by_xpath('//div[@id="FurnishID"]/div[@class="makeSelect"]/select/option[@label="Unfurnished"]').click()
		self.driver.implicitly_wait(20)
		time.sleep(2)

		tot_flr = self.driver.find_element_by_xpath('//div[@id="Total_FloorID"]/div/select/option[@label="20"]').click()
		self.driver.implicitly_wait(20)
		time.sleep(2)

		flrNo = self.driver.find_element_by_xpath('//div[@id="Floor_NumID"]/div/select/option[@label="3"]').click()
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

		monthrent = self.driver.find_element_by_xpath('//div[@id="RentID"]/input')
		act_monthrent = ActionChains(self.driver)
		act_monthrent.move_to_element(monthrent)
		act_monthrent.click(monthrent)
		act_monthrent.send_keys('20000').perform()
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
		act_detail.send_keys('Spacious flat with all modern amenities. Great for family. We will get the modular kitchen made. ').perform()
		self.driver.implicitly_wait(20)
		time.sleep(2)

		next4 = self.driver.find_element_by_xpath('//button[@class="primaryButton ng-binding"]').click()
		self.driver.implicitly_wait(20)
		time.sleep(2)

		#submit = self.driver.find_element_by_xpath('//button[@class="primaryButton ng-binding"]').click()
		#self.driver.implicitly_wait(20)
		

		time.sleep(2)
		self.driver.quit()
		time.sleep(3)

		self.__init__()
		self.driver.get('http://property.sulekha.com/post-your-property')
		self.driver.implicitly_wait(20)
		self.driver.maximize_window()
		self.driver.implicitly_wait(10)

		login = self.driver.find_element_by_id('sul_ressignin').click()
		self.driver.implicitly_wait(20)
		time.sleep(2)

		self.driver.switch_to.frame(self.driver.find_element_by_tag_name('iframe'))

		email = self.driver.find_element_by_id('txtuname')
		email.send_keys('prathamsawant115@gmail.com')
		self.driver.implicitly_wait(20)
		time.sleep(2)

		passw = self.driver.find_element_by_id('txtpwd')
		passw.send_keys('nx1234')
		self.driver.implicitly_wait(20)
		time.sleep(2)

		sign = self.driver.find_element_by_id('btnsignin').click()
		self.driver.implicitly_wait(20)
		time.sleep(2)

		iam = self.driver.find_element_by_xpath('//div[@class="form-group"]/div/ul/li[3]').click()
		self.driver.implicitly_wait(20)
		time.sleep(2)

		rent = self.driver.find_element_by_xpath('//div[@class="form-group"]/div[@class="manage-menu tabs"]/ul/li[@data-value="Rentals"]/a').click()
		self.driver.implicitly_wait(20)
		time.sleep(2)

		proc = self.driver.find_element_by_xpath('//div[@class="action"]/a').click()
		self.driver.implicitly_wait(20)
		time.sleep(2)'''

		time.sleep(10)
		self.driver.quit()
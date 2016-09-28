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


class Makaan(CrawlSpider):
	name = 'makkanPosting'
	allowed_domains = ['makaan.com']
	start_urls = ['http://www.makaan.com']
	#'locality':'','sub_loc':'','sqft':'','rent_price':'','title':'','detail':'','bed':'','flr':'','t_flr':'','depo':'','status':'','email':''
	
	def __init__(self):
		self.driver = webdriver.Chrome()
		MONGODB_SERVER = "localhost"
		MONGODB_PORT = 27017
		# MONGODB_DB = "scraping"
		# MONGODB_COLLECTION = "scrape"
		connection = pymongo.MongoClient(MONGODB_SERVER,MONGODB_PORT)
		db = connection['scrapingandposting']
		self.collection_B = db['Bandra']

	def parse(self,response):
		t1=t2=t3=t4=0
		data_post = list(self.collection_B.find().limit(40))#[]
		# data1 = list(self.collection_B.find().limit(18))
		# data2 = list(self.collection_s.find().limit(18))
		# for n in range(0,len(data1)):
		# 	if ((n%4==0) or (n%4==1)):
		# 		data_post.append(data1[n])
		# 		data_post.append(data2[n])
		# 	if ((n%4==2) or (n%4==3)):
		# 		data_post.append(data2[n])
		# 		data_post.append(data1[n])
		#print data_post
		for i in range(0,len(data_post)):
			if (not i==0):
				self.__init__()
			self.driver.get(response.url)
			self.driver.implicitly_wait(40)
			time.sleep(3)

			login = self.driver.find_element_by_xpath('//div[@data-type="sell-your-property"]/a')
			login.click()
			self.driver.implicitly_wait(10)
			time.sleep(4)

			logemail = self.driver.find_element_by_xpath('//div[@class="login-btn-style max-width220"]')
			logemail.click()
			self.driver.implicitly_wait(10)
			time.sleep(4)

			if (i%4==0):
				emailid = self.driver.find_element_by_id('username')
				emailid.send_keys('prathamsawant115@gmail.com')
				self.driver.implicitly_wait(20)
				time.sleep(3)
				t1=t1+1
			if (i%4==1):
				emailid = self.driver.find_element_by_id('username')
				emailid.send_keys('oyeok.noreply3@gmail.com')
				self.driver.implicitly_wait(20)
				time.sleep(3)
				t2=t2+1
			if (i%4==2):
				emailid = self.driver.find_element_by_id('username')
				emailid.send_keys('oyeok.hi3@gmail.com')
				self.driver.implicitly_wait(20)
				time.sleep(3)
				t3=t3+1
			if (i%4==3):
				emailid = self.driver.find_element_by_id('username')
				emailid.send_keys('oyeok.realestate2@gmail.com')
				self.driver.implicitly_wait(20)
				time.sleep(3)
				t4=t4+1

			passw = self.driver.find_element_by_id('password')
			passw.send_keys('nx1234')
			self.driver.implicitly_wait(20)
			time.sleep(3)

			loginbut = self.driver.find_element_by_xpath('//div[@data-type="login-btn"]')
			loginbut.click()
			self.driver.implicitly_wait(20)
			time.sleep(3)

			listing = self.driver.find_element_by_xpath('//a[@data-type="list-property"]')
			listing.click()
			self.driver.implicitly_wait(20)
			time.sleep(3)

			rent = self.driver.find_element_by_xpath('//li[@data-sellrent="rent"]')
			rent.click()
			self.driver.implicitly_wait(20)
			time.sleep(3)

			locality = self.driver.find_element_by_id('localityMap')
			locality.click()
			self.driver.implicitly_wait(10)
			time.sleep(3)

			local = self.driver.find_element_by_xpath('//input[@class="search-bar-locality"]')
			self.driver.implicitly_wait(15)
			local.send_keys(data_post[i]['locality'])
			self.driver.implicitly_wait(10)
			time.sleep(3)

			loc = self.driver.find_element_by_xpath('//div[@id="search-results"]/ul/li[1]')
			self.driver.implicitly_wait(10)
			loc.click()
			time.sleep(3)

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
			time.sleep(3)

			apar = self.driver.find_element_by_xpath('//li[@data-value="Apartment"]')
			action_apar = ActionChains(self.driver)
			action_apar.move_to_element(apar)
			action_apar.click(apar).perform()
			self.driver.implicitly_wait(10)
			time.sleep(3)

			bed = self.driver.find_element_by_id('bed')
			action_bed = ActionChains(self.driver)
			action_bed.move_to_element(bed)
			action_bed.click(bed).click(bed).perform()
			self.driver.implicitly_wait(10)
			time.sleep(3)

			bedroom = self.driver.find_element_by_xpath('//li[@data-value="'+data_post[i]['bed']+'"]')
			action_bedroom = ActionChains(self.driver)
			action_bedroom.move_to_element(bedroom)
			action_bedroom.click(bedroom).perform()
			time.sleep(3)

			area = self.driver.find_element_by_id('area')
			action_area = ActionChains(self.driver)
			action_area.move_to_element(area)
			action_area.click(area).click(area)
			action_area.send_keys(data_post[i]['sqft']).perform()
			time.sleep(3)

			month = self.driver.find_element_by_id('rentPrice')
			action_month = ActionChains(self.driver)
			action_month.move_to_element(month)
			action_month.click(month)
			if '.' in data_post[i]['rent_price']:
				data_post[i]['rent_price'] = data_post[i]['rent_price'].split('.')[0]
				data_post[i]['rent_price'] = str(int(data_post[i]['rent_price'])+2000)
			else:
				data_post[i]['rent_price'] = str(int(data_post[i]['rent_price'])+2000)
			action_month.send_keys(data_post[i]['rent_price']).perform()
			time.sleep(3)

			nego = self.driver.find_element_by_xpath('//div[@data-type="negotiable"]/div/label')
			nego.click()
			self.driver.implicitly_wait(20)
			time.sleep(3)

			secr = self.driver.find_element_by_id('securityDeposit')
			action_secr = ActionChains(self.driver)
			action_secr.move_to_element(secr)
			action_secr.click(secr)
			if '.' in data_post[i]['depo']:
				data_post[i]['depo'] = data_post[i]['depo'].split('.')[0]
			action_secr.send_keys(data_post[i]['depo']).perform()
			self.driver.implicitly_wait(20)
			time.sleep(3)

			# avial = self.driver.find_element_by_xpath('//input[@id="availableFrom"]')
			# action_avail = ActionChains(self.driver)
			# action_avail.move_to_element(avial).move_to_element(avial)
			# action_avail.click(avial).click(avial)
			# self.driver.implicitly_wait(20)
			# time.sleep(3)

			# sele_avail = self.driver.find_element_by_xpath('//td[@class="is-today is-selected"]/button')
			# action_sele = ActionChains(self.driver)
			# action_sele.move_to_element(sele_avail)
			# action_sele.click(sele_avail)
			# self.driver.implicitly_wait(20)
			# time.sleep(3)

			decs = self.driver.find_element_by_id('Description')
			action_decs = ActionChains(self.driver)
			action_decs.move_to_element(decs)
			action_decs.click(decs)
			action_decs.send_keys(data_post[i]['detail']).perform()
			time.sleep(3)

			if 'Unfurnished' in data_post[i]['status']:
				stat = self.driver.find_element_by_xpath('//label[@for="unFurnished"]')
				action_stat = ActionChains(self.driver)
				action_stat.move_to_element(stat)
				action_stat.click(stat).perform()
				time.sleep(3)
			elif 'Semi-Furnished' in data_post[i]['status']:
				stat = self.driver.find_element_by_xpath('//label[@for="semiFurnished"]')
				act_fur = ActionChains(self.driver)
				act_fur.move_to_element(stat)
				act_fur.click(stat).perform()
				self.driver.implicitly_wait(20)
				time.sleep(3)

				fur1 = self.driver.find_element_by_xpath('//li[@data-icon-id="furnishing_icon_bed"]')
				act_fur1 = ActionChains(self.driver)
				act_fur1.move_to_element(fur1)
				act_fur1.click(fur1).perform()
				self.driver.implicitly_wait(20)
				time.sleep(3)

				fur3 = self.driver.find_element_by_xpath('//li[@data-icon-id="furnishing_icon_tv"]')
				act_fur3 = ActionChains(self.driver)
				act_fur3.move_to_element(fur3)
				act_fur3.click(fur3).perform()
				self.driver.implicitly_wait(20)
				time.sleep(3)

				fur4 = self.driver.find_element_by_xpath('//li[@data-icon-id="furnishing_icon_sofa"]')
				act_fur4 = ActionChains(self.driver)
				act_fur4.move_to_element(fur4)
				act_fur4.click(fur4).perform()
				self.driver.implicitly_wait(20)
				time.sleep(3)
			elif 'Furnished' in data_post[i]['status']:
				stat = self.driver.find_element_by_xpath('//label[@for="furnished"]')
				act_fur = ActionChains(self.driver)
				act_fur.move_to_element(stat)
				act_fur.click(stat).perform()
				time.sleep(3)

				fur1 = self.driver.find_element_by_xpath('//li[@data-icon-id="furnishing_icon_bed"]')
				act_fur1 = ActionChains(self.driver)
				act_fur1.move_to_element(fur1)
				act_fur1.click(fur1).perform()
				self.driver.implicitly_wait(20)
				time.sleep(3)

				fur2 = self.driver.find_element_by_xpath('//li[@data-icon-id="furnishing_icon_ac"]')
				act_fur2 = ActionChains(self.driver)
				act_fur2.move_to_element(fur2)
				act_fur2.click(fur2).perform()
				self.driver.implicitly_wait(20)
				time.sleep(3)

				fur3 = self.driver.find_element_by_xpath('//li[@data-icon-id="furnishing_icon_tv"]')
				act_fur3 = ActionChains(self.driver)
				act_fur3.move_to_element(fur3)
				act_fur3.click(fur3).perform()
				self.driver.implicitly_wait(20)
				time.sleep(3)

				fur4 = self.driver.find_element_by_xpath('//li[@data-icon-id="furnishing_icon_sofa"]')
				act_fur4 = ActionChains(self.driver)
				act_fur4.move_to_element(fur4)
				act_fur4.click(fur4).perform()
				self.driver.implicitly_wait(20)
				time.sleep(3)

				fur5 = self.driver.find_element_by_xpath('//li[@data-icon-id="furnishing_icon_wifi-connection"]')
				action_fur5 = ActionChains(self.driver)
				action_fur5.move_to_element(fur5)
				action_fur5.click(fur5).perform()
				time.sleep(3)

			amen1 = self.driver.find_element_by_xpath('//li[@data-icon-id="amenities_icon_parking"]')
			action_amen1 = ActionChains(self.driver)
			action_amen1.move_to_element(amen1)
			action_amen1.click(amen1).perform()
			time.sleep(3)

			amen2 = self.driver.find_element_by_xpath('//li[@data-icon-id="amenities_icon_lift"]')
			action_amen2 = ActionChains(self.driver)
			action_amen2.move_to_element(amen2)
			action_amen2.click(amen2).perform()
			time.sleep(3)

			amen3 = self.driver.find_element_by_xpath('//li[@data-icon-id="amenities_icon_power-backup"]')
			action_amen3 = ActionChains(self.driver)
			action_amen3.move_to_element(amen3)
			action_amen3.click(amen3).perform()
			time.sleep(3)

			amen4 = self.driver.find_element_by_xpath('//li[@data-icon-id="amenities_icon_swimming-pool"]')
			action_amen4 = ActionChains(self.driver)
			action_amen4.move_to_element(amen4)
			action_amen4.click(amen4).perform()
			time.sleep(3)

			amen5 = self.driver.find_element_by_xpath('//li[@data-icon-id="amenities_icon_garden-park"]')
			action_amen5 = ActionChains(self.driver)
			action_amen5.move_to_element(amen5)
			action_amen5.click(amen5).perform()
			time.sleep(3)

			amen6 = self.driver.find_element_by_xpath('//li[@data-icon-id="amenities_icon_gym"]')
			action_amen6 = ActionChains(self.driver)
			action_amen6.move_to_element(amen6)
			action_amen6.click(amen6).perform()
			time.sleep(3)

			amen7 = self.driver.find_element_by_xpath('//li[@data-icon-id="amenities_icon_maintenance-staff"]')
			action_amen7 = ActionChains(self.driver)
			action_amen7.move_to_element(amen7)
			action_amen7.click(amen7).perform()
			time.sleep(3)

			pref = self.driver.find_element_by_xpath('//li[@data-icon-id="tenants_icon_family"]')
			action_pref = ActionChains(self.driver)
			action_pref.move_to_element(pref)
			action_pref.click(pref).perform()
			time.sleep(3)

			prop_det = self.driver.find_element_by_xpath('//div[@class="accordian-box js-accordian-box"]/h3')
			action_prop_det = ActionChains(self.driver)
			action_prop_det.move_to_element(prop_det)
			action_prop_det.click(prop_det).perform()
			time.sleep(3)

			bathroom = self.driver.find_element_by_id('bathroom')
			action_bathroom = ActionChains(self.driver)
			action_bathroom.move_to_element(bathroom)
			action_bathroom.click(bathroom).perform()
			time.sleep(3)

			select_bath = self.driver.find_element_by_xpath('//div[@style="z-index: 999; position: absolute;"]/div/ul/li[@data-value="'+data_post[i]['bed']+'"]')
			action_select_bath = ActionChains(self.driver)
			action_select_bath.move_to_element(select_bath)
			action_select_bath.click(select_bath).perform()
			time.sleep(2)

			bal = self.driver.find_element_by_id('balconies')
			action_bal = ActionChains(self.driver)
			action_bal.move_to_element(bal)
			action_bal.click(bal).click(bal).perform()
			time.sleep(2)

			select_bal = self.driver.find_element_by_xpath('//div[@style="z-index: 999; position: absolute;"]/div/ul/li[@data-value="'+data_post[i]['bed']+'"]')
			action_select_bal = ActionChains(self.driver)
			action_select_bal.move_to_element(select_bal)
			action_select_bal.click(select_bal).perform()
			time.sleep(2)

			floor = self.driver.find_element_by_id('f-no')
			action_floor = ActionChains(self.driver)
			action_floor.move_to_element(floor)
			action_floor.click(floor).click(floor).perform()
			time.sleep(2)

			sel_flr = self.driver.find_element_by_xpath('//div[@style="z-index: 999; position: absolute;"]/div/ul/li[@data-value="'+data_post[i]['flr']+'"]')
			action_sel_flr = ActionChains(self.driver)
			action_sel_flr.move_to_element(sel_flr)
			action_sel_flr.click(sel_flr).perform()
			time.sleep(2)

			tot_flr = self.driver.find_element_by_id('total-f')
			action_tot_flr = ActionChains(self.driver)
			action_tot_flr.move_to_element(tot_flr)
			action_tot_flr.click(tot_flr).click(tot_flr).perform()
			time.sleep(2)

			if len(data_post[i]['t_flr'])>2:
				data_post[i]['t_flr'] = str(int(data_post[i]['flr'])+3)
			sel_tot_flr = self.driver.find_element_by_xpath('//div[@style="z-index: 999; position: absolute;"]/div/ul/li[@data-value="'+data_post[i]['t_flr']+'"]')
			action_sel_tot_flr = ActionChains(self.driver)
			action_sel_tot_flr.move_to_element(sel_tot_flr)
			action_sel_tot_flr.click(sel_tot_flr).perform()
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

			add_later = self.driver.find_element_by_xpath('//div[@class="action-btn-wrap"]/span')
			action_add = ActionChains(self.driver)
			action_add.move_to_element(add_later)
			action_add.click(add_later).perform()
			time.sleep(2)

			submit = self.driver.find_element_by_xpath('//div[@class="action-btn-holder"]/div')
			act_sub = ActionChains(self.driver)
			act_sub.move_to_element(submit)
			act_sub.click(submit).perform()
			self.driver.implicitly_wait(20)

			print "+++++++++++++++++++++++++++++++"
			print 'Posted '+str(i)
			print 'prathamsawant115' + ' = ' + str(t1)
			print 'oyeok.noreply3' + ' = ' + str(t2)
			print 'oyeok.hi3' + ' = ' + str(t3)
			print 'oyeok.realestate2' + ' = ' + str(t4)
			print "+++++++++++++++++++++++++++++++"

			time.sleep(15)
			self.driver.quit()
			time.sleep(15)
			if i%4==0:
				time.sleep(30)
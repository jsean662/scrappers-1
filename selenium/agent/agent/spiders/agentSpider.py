import scrapy
from selenium import webdriver
from scrapy.spiders import CrawlSpider
from scrapy.http import Request
from agent.items import AgentItem
from selenium.webdriver.common.action_chains import ActionChains
from scrapy.selector import Selector
import time
from datetime import datetime as dt

class MagicAgent(CrawlSpider):
	name = 'agentSpider'
	allowed_domains = ['magicbricks.com']

	start_urls = ['http://www.magicbricks.com/Real-estate-property-agents/agent-in-Mumbai/Page-5?proptype=Multistorey-Apartment,Builder-Floor-Apartment,Penthouse,Studio-Apartment,Residential-House,Villa,Commercial-Office-Space,Office-in-IT-Park/-SEZ,Commercial-Shop,Commercial-Showroom,Commercial-Land,Industrial-Land&Locality=Andheri-West,Bandra-West,4-Bunglows&dealingIn=Rent-Lease&nsrSearchBar=N&searchTransMode=driving&bar_propertyType_R_new=10002_10003_10021_10022_10020,10001_10017,10007_10018,10008_10009,10006_10012&category=R&price=Y&bar_propertyType_new=10002_10003_10021_10022_10020,10001_10017,10007_10018,10008_10009,10006_10012&mbTrackSrc=agentHomeSearchForm&tab1=agent']
	item = AgentItem()
	count = 1

	def parse(self , response):
		driver = webdriver.Chrome()

		driver.get(response.url)

		driver.implicitly_wait(30)
		#f = open('agents.csv','ab')
		#f.write('Name,Company,Phone,Emails,"Date of Addition"\n')
		#f.close()
		cont = driver.find_elements_by_xpath('//div[@class="srpBlock"]')
		
		for c in cont:
			self.item['company'] = c.find_element_by_xpath('div[@class="proDetail"]/div[@class="proNameAndPrice"]/div[@class="proName"]/p[@class="proHeading"]/strong').text
			self.item['agent_name'] = c.find_element_by_xpath('div[@class="proDetail"]/div[@class="proNameAndPrice"]/div[@class="proName"]/p[@class="proGroup"]').text.replace('Contact Person: ','')
			driver.implicitly_wait(30)
			try:
				buttn = c.find_element_by_xpath('div[@class="srpBtnWrap"]/div[@class="srpBlockLeftBtn"]/ul/li[2]/a')
				act_butt = ActionChains(driver)
				act_butt.move_to_element(buttn)
				act_butt.click(buttn).perform()
				driver.implicitly_wait(30)
			except:
				print 'No Button'
			if (self.count==1) and ('display: block;' in c.find_element_by_xpath('div[@class="srpBtnWrap"]/div[@class="contactForms"]/div[@class="formsWrap viewPhoneForm"]').get_attribute('style')):
				ind = c.find_element_by_xpath('div[@class="srpBtnWrap"]/div[@class="contactForms"]/div[@class="formsWrap viewPhoneForm"]/div[@class=" "]/div[@class="formCont propUpdatePop forForm"]/div[@class="formCont propUpdatePop"]/form/div/div[@class="formBlock"]/ul/li[1]/div[@class="userType"]/div[@class="formValue usetype"]/label[2]')
				act_ind = ActionChains(driver)
				act_ind.move_to_element(ind)
				act_ind.click(ind).perform()
				driver.implicitly_wait(20)

				name = c.find_element_by_xpath('div[@class="srpBtnWrap"]/div[@class="contactForms"]/div[@class="formsWrap viewPhoneForm"]/div[@class=" "]/div[@class="formCont propUpdatePop forForm"]/div[@class="formCont propUpdatePop"]/form/div/div[@class="formBlock"]/ul/li[2]/div[@class="formValue"]/input')
				act_name = ActionChains(driver)
				act_name.move_to_element(name)
				act_name.click(name)
				act_name.send_keys('pratham').perform()
				driver.implicitly_wait(40)
				time.sleep(5)

				mob = c.find_element_by_xpath('div[@class="srpBtnWrap"]/div[@class="contactForms"]/div[@class="formsWrap viewPhoneForm"]/div[@class=" "]/div[@class="formCont propUpdatePop forForm"]/div[@class="formCont propUpdatePop"]/form/div/div[@class="formBlock"]/ul/li[3]/div[@class="formValue"]/div[@class="ftlt"]/input')
				act_mob = ActionChains(driver)
				act_mob.move_to_element(mob)
				act_mob.click(mob)
				act_mob.send_keys('9702293897').perform()
				driver.implicitly_wait(40)
				time.sleep(8)

				email = c.find_element_by_xpath('div[@class="srpBtnWrap"]/div[@class="contactForms"]/div[@class="formsWrap viewPhoneForm"]/div[@class=" "]/div[@class="formCont propUpdatePop forForm"]/div[@class="formCont propUpdatePop"]/form/div/div[@class="formBlock"]/ul/li[4]/div[@class="formValue"]/input')
				act_email = ActionChains(driver)
				act_email.move_to_element(email)
				act_email.click(email)
				act_email.send_keys('prathamsawant115@gmail.com').perform()
				driver.implicitly_wait(40)
				time.sleep(15)

				view = c.find_element_by_xpath('div[@class="srpBtnWrap"]/div[@class="contactForms"]/div[@class="formsWrap viewPhoneForm"]/div[@class=" "]/div[@class="formCont propUpdatePop forForm"]/div[@class="formCont propUpdatePop"]/form/div/div[@class="formBlock"]/ul/li[@class="actionCont"]')
				act_view = ActionChains(driver)
				act_view.move_to_element(view)
				act_view.click(view).perform()
				driver.implicitly_wait(40)
				time.sleep(8)

				if "pupWrap popContainer" in driver.page_source:
					driver.quit()
					time.sleep(2)
				
				dig = c.find_element_by_id('smsNo')
				act_dig = ActionChains(driver)
				act_dig.move_to_element(dig)
				act_dig.click(dig)
				act_dig.send_keys('296').perform()
				driver.implicitly_wait(40)
				time.sleep(8)

				press = c.find_element_by_xpath('div[@class="srpBtnWrap"]/div[@class="contactForms"]/div[@class="formsWrap viewPhoneForm"]/div[@class=" "]/div[@class="formStep3 formCont propUpdatePop"]/div/div/div[@class="verifyBlock"]/div[@class="actionBlock"]/a')
				act_press = ActionChains(driver)
				act_press.move_to_element(press)
				act_press.click(press).perform()
				driver.implicitly_wait(40)
				self.count = 0
				time.sleep(2)
			
			if "pupWrap popContainer" in driver.page_source:
				driver.quit()
				time.sleep(2)

			try:
				self.item['phone'] = c.find_element_by_xpath('div[@class="srpBtnWrap"]/div[@class="contactForms"]/div[@class="formsWrap viewPhoneForm"]/div[@class=" "]/div[@class="newSimilarForDetail"]/div/div[@class="infoCont"]/div[@class="localText"]/div[@class="contact"]/div[contains(@id,"mobileDiv")]/strong').text
			except:
				self.item['phone'] = 'None'
			if ',' in self.item['phone']:
				self.item['phone'] = self.item['phone'].replace(',',';')
			f = open('agents.csv','ab')
			f.write('"'+self.item['agent_name']+'","'+self.item['company']+'",'+self.item['phone']+',"sample@sample.com","'+dt.strftime(dt.now(),'%Y-%m-%d %H:%M:%S')+'"'+'\n')
			f.close()
			driver.implicitly_wait(30)
			print "++++++++++++++++++++++++++++++++++++++"
			print self.item
			print "++++++++++++++++++++++++++++++++++++++"
			time.sleep(20)

		driver.quit()
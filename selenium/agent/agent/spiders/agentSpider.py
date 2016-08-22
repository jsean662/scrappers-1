import scrapy
from selenium import webdriver
from scrapy.spiders import CrawlSpider
from agent.items import AgentItem
from selenium.webdriver.common.action_chains import ActionChains
from scrapy.selector import Selector
import time

class MagicAgent(CrawlSpider):
	name = 'agentSpider'
	allowed_domains = ['magicbricks.com']

	start_urls = ['http://www.magicbricks.com/Real-estate-property-agents/agent-in-Mumbai?proptype=Multistorey-Apartment,Builder-Floor-Apartment,Penthouse,Studio-Apartment,Residential-House,Villa,Commercial-Office-Space,Office-ITPark-SEZ,Commercial-Shop,Commercial-Showroom,Commercial-Land,Industrial-Land&Locality=Andheri-West,Bandra-West,Four-Bungalows,Seven-Bungalows&dealingIn=Rent-Lease']
	item = AgentItem()

	def parse(self , response):
		driver = webdriver.Chrome()

		driver.get(response.url)

		driver.implicitly_wait(30)
		count = 1

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
			if (count==1) and ('display: block;' in c.find_element_by_xpath('div[@class="srpBtnWrap"]/div[@class="contactForms"]/div[@class="formsWrap viewPhoneForm"]').get_attribute('style')):
				ind = c.find_element_by_xpath('div[@class="srpBtnWrap"]/div[@class="contactForms"]/div[@class="formsWrap viewPhoneForm"]/div[@class=" "]/div[@class="formCont propUpdatePop forForm"]/div[@class="formCont propUpdatePop"]/form/div/div[@class="formBlock"]/ul/li[1]/div[@class="userType"]/div[@class="formValue usetype"]/label[2]')
				act_ind = ActionChains(driver)
				act_ind.move_to_element(ind)
				act_ind.click(ind).perform()
				driver.implicitly_wait(20)

				name = c.find_element_by_xpath('div[@class="srpBtnWrap"]/div[@class="contactForms"]/div[@class="formsWrap viewPhoneForm"]/div[@class=" "]/div[@class="formCont propUpdatePop forForm"]/div[@class="formCont propUpdatePop"]/form/div/div[@class="formBlock"]/ul/li[2]/div[@class="formValue"]/input')
				act_name = ActionChains(driver)
				act_name.move_to_element(name)
				act_name.click(name)
				act_name.send_keys('shlok').perform()
				driver.implicitly_wait(40)
				time.sleep(5)

				mob = c.find_element_by_xpath('div[@class="srpBtnWrap"]/div[@class="contactForms"]/div[@class="formsWrap viewPhoneForm"]/div[@class=" "]/div[@class="formCont propUpdatePop forForm"]/div[@class="formCont propUpdatePop"]/form/div/div[@class="formBlock"]/ul/li[3]/div[@class="formValue"]/div[@class="ftlt"]/input')
				act_mob = ActionChains(driver)
				act_mob.move_to_element(mob)
				act_mob.click(mob)
				act_mob.send_keys('9769036234').perform()
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
					print "+++++++++++++++++++++++++++++++"
					print 'got it'
					print '+++++++++++++++++++++++++++++++'
					

				dig = c.find_element_by_id('smsNo')
				act_dig = ActionChains(driver)
				act_dig.move_to_element(dig)
				act_dig.click(dig)
				act_dig.send_keys('190').perform()
				driver.implicitly_wait(40)
				time.sleep(8)

				press = c.find_element_by_xpath('div[@class="srpBtnWrap"]/div[@class="contactForms"]/div[@class="formsWrap viewPhoneForm"]/div[@class=" "]/div[@class="formStep3 formCont propUpdatePop"]/div/div/div[@class="verifyBlock"]/div[@class="actionBlock"]/a')
				act_press = ActionChains(driver)
				act_press.move_to_element(press)
				act_press.click(press).perform()
				driver.implicitly_wait(40)
				count = 0

			try:
				self.item['phone'] = c.find_element_by_xpath('div[@class="srpBtnWrap"]/div[@class="contactForms"]/div[@class="formsWrap viewPhoneForm"]/div[@class=" "]/div[@class="newSimilarForDetail"]/div/div[@class="infoCont"]/div[@class="localText"]/div[@class="contact"]/div').text
			except:
				self.item['phone'] = None

			f =open('agent','ab')
			f.write("company:"+self.item['company']+" "+"agent_name:"+self.item['agent_name']+" "+"phone:"+self.item['phone']+"\n")
			f.close()
			driver.implicitly_wait(30)
			print self.item
			time.sleep(20)

		driver.quit()
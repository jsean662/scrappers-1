from scrapy.spiders import CrawlSpider
from selenium import webdriver
from scrapy.http import FormRequest
from scrapy.selector import Selector
from scrapy.utils.response import open_in_browser
import datetime
import time
import smtplib
import os
import pymongo
from scrapy import log

class OlxForm(CrawlSpider):
	name = 'olxSpider'
	allowed_domains = ['olx.in']
	start_urls = ['https://www.olx.in/']

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
		t1=t2=t3=t4=t5=t6=t7=t8=0
		add = 0
		data_post = list(self.collection_a.find().limit(40))
		#a=40
		for i in range(0,len(data_post)):
			if i%8==0:
				add = add + 1000
			if (not i==0):
				self.__init__()
			self.driver.get(response.url)
			self.driver.implicitly_wait(40)

			accnt = self.driver.find_element_by_id('my-account-link').click()
			self.driver.implicitly_wait(20)
			time.sleep(2)

			if i%8==0:
				email = self.driver.find_element_by_id('userEmail')
				email.send_keys('9029618053')
				self.driver.implicitly_wait(20)
				time.sleep(2)
				t1=t1+1
			if i%8==1:
				email = self.driver.find_element_by_id('userEmail')
				email.send_keys('9702293897')
				self.driver.implicitly_wait(20)
				time.sleep(2)
				t2=t2+1
			if i%8==2:
				email = self.driver.find_element_by_id('userEmail')
				email.send_keys('7715093028')
				self.driver.implicitly_wait(20)
				time.sleep(2)
				t3=t3+1
			if i%8==3:
				email = self.driver.find_element_by_id('userEmail')
				email.send_keys('9869848979')
				self.driver.implicitly_wait(20)
				time.sleep(2)
				t4=t4+1
			if i%8==4:
				email = self.driver.find_element_by_id('userEmail')
				email.send_keys('7715093181')
				self.driver.implicitly_wait(20)
				time.sleep(2)
				t5=t5+1
			if i%8==5:
				email = self.driver.find_element_by_id('userEmail')
				email.send_keys('7715093035')
				self.driver.implicitly_wait(20)
				time.sleep(2)
				t6=t6+1
			if i%8==6:
				email = self.driver.find_element_by_id('userEmail')
				email.send_keys('7715093176')
				self.driver.implicitly_wait(20)
				time.sleep(2)
				t7=t7+1
			if i%8==7:
				email = self.driver.find_element_by_id('userEmail')
				email.send_keys('7715093067')
				self.driver.implicitly_wait(20)
				time.sleep(2)
				t8=t8+1

			passwd = self.driver.find_element_by_id('userPass')
			passwd.send_keys('nx1234')
			self.driver.implicitly_wait(20)
			time.sleep(3)

			login = self.driver.find_element_by_id('se_userLogin').click()
			self.driver.implicitly_wait(20)
			time.sleep(3)

			click_on_ad = self.driver.find_element_by_id('postNewAdLink').click()
			self.driver.implicitly_wait(20)
			time.sleep(3)

			title = self.driver.find_element_by_id('add-title')
			title.send_keys(data_post[i]['title'])
			self.driver.implicitly_wait(20)
			time.sleep(3)

			catgry = self.driver.find_element_by_id('targetrenderSelect1-0').click()
			self.driver.implicitly_wait(20)
			time.sleep(3)

			sel_cat = self.driver.find_element_by_id('cat-1309').click()
			self.driver.implicitly_wait(20)
			time.sleep(3)

			price = self.driver.find_element_by_name('data[param_price][1]')
			if '.' in data_post[i]['rent_price']:
				data_post[i]['rent_price'] = data_post[i]['rent_price'].split('.')[0]
				data_post[i]['rent_price'] = str(int(data_post[i]['rent_price'])+add)
			else:
				data_post[i]['rent_price'] = str(int(data_post[i]['rent_price'])+add)
			price.send_keys(data_post[i]['rent_price'])
			self.driver.implicitly_wait(20)
			time.sleep(3)

			furnsh = self.driver.find_element_by_id('targetparam15').click()
			self.driver.implicitly_wait(20)
			time.sleep(2)

			if 'Furnished' in data_post[i]['status']:
				sel_furnsh = self.driver.find_element_by_xpath('//dl[@id="targetparam15"]/dd/ul/li[2]/a').click()
				self.driver.implicitly_wait(20)
				time.sleep(2)
			else:
				sel_furnsh = self.driver.find_element_by_xpath('//dl[@id="targetparam15"]/dd/ul/li[3]/a').click()
				self.driver.implicitly_wait(20)
				time.sleep(2)

			bed = self.driver.find_element_by_id('targetparam17').click()
			self.driver.implicitly_wait(20)
			time.sleep(2)

			if '1' in data_post[i]['bed']:
				sel_bed = self.driver.find_element_by_xpath('//dl[@id="targetparam17"]/dd/ul/li[2]/a').click()
				self.driver.implicitly_wait(20)
				time.sleep(2)
			if '2' in data_post[i]['bed']:
				sel_bed = self.driver.find_element_by_xpath('//dl[@id="targetparam17"]/dd/ul/li[3]/a').click()
				self.driver.implicitly_wait(20)
				time.sleep(2)
			if '3' in data_post[i]['bed']:
				sel_bed = self.driver.find_element_by_xpath('//dl[@id="targetparam17"]/dd/ul/li[4]/a').click()
				self.driver.implicitly_wait(20)
				time.sleep(2)
			if '4' in data_post[i]['bed']:
				sel_bed = self.driver.find_element_by_xpath('//dl[@id="targetparam17"]/dd/ul/li[5]/a').click()
				self.driver.implicitly_wait(20)
				time.sleep(2)

			area = self.driver.find_element_by_id('param325')
			area.send_keys(data_post[i]['sqft'])
			self.driver.implicitly_wait(20)
			time.sleep(2)

			desc = self.driver.find_element_by_id('add-description')
			desc.send_keys('Nice appartment and locality'+data_post[i]['detail'])

			for root,dirs,files in os.walk('/home/karan/scrap_proj/selenium/Postings_photos/1/'+str((i%18)+1)+'/'):
				for name in files:
					if '1' in name:
						path1 = root+name
					if '2' in name:
						path2 = root+name
					if '3' in name:
						path3 = root+name

			add_photo = self.driver.find_element_by_id('show-gallery-html').click()
			self.driver.implicitly_wait(20)
			time.sleep(3)

			img1 = self.driver.find_element_by_name('image[1]')
			img1.send_keys(path1)
			self.driver.implicitly_wait(20)
			time.sleep(2)

			img2 = self.driver.find_element_by_name('image[2]')
			img2.send_keys(path2)
			self.driver.implicitly_wait(20)
			time.sleep(2)

			img3 = self.driver.find_element_by_name('image[3]')
			img3.send_keys(path3)
			self.driver.implicitly_wait(20)
			time.sleep(2)

			# submit = self.driver.find_element_by_id('save').click()
			# self.driver.implicitly_wait(20)
			# time.sleep(3)

			print "+++++++++++++++++++++++++++++++"
			print "Posted "+str(i)
			print '9029618053 = '+str(t1)
			print '9702293897 = '+str(t2)
			print '7715093028 = '+str(t3)
			print '9869848979 = '+str(t4)
			print '7715093181 = '+str(t5)
			print '7715093035 = '+str(t6)
			print '7715093176 = '+str(t7)
			print '7715093067 = '+str(t8)
			print "+++++++++++++++++++++++++++++++"

			# del data_post[i]['_id']
			# data_post[i].update({'date':str(datetime.date.today())})
			# self.collection_p.insert(dict(data_post[i]))
			# log.msg("Posted Data added to MongoDB database!",level=log.DEBUG)
			
			time.sleep(15)
			self.driver.quit()
			time.sleep(15)
			if i%4==0:
				time.sleep(30)
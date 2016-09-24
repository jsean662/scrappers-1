from scrapy.spiders import CrawlSpider
from selenium import webdriver
from scrapy.http import FormRequest
from scrapy.selector import Selector
from scrapy.utils.response import open_in_browser
import datetime
import time
import smtplib
import pymongo
from scrapy import log

class Contact(CrawlSpider):
	name = 'quikrSpider'
	allowed_domains = ['quikr.com']
	start_urls = ['http://www.quikr.com/homes/postad']
	#'locality':'','sub_loc':'','sqft':'','rent_price':'','title':'','detail':'','bed':'','flr':'','t_flr':'','depo':'','status':'','email':''
	
	def __init__(self):
		self.driver = webdriver.Chrome()
		MONGODB_SERVER = "localhost"
		MONGODB_PORT = 27017
		# MONGODB_DB = "scraping"
		# MONGODB_COLLECTION = "scrape"
		connection = pymongo.MongoClient(MONGODB_SERVER,MONGODB_PORT)
		db = connection['scrapingandposting']
		self.collection_A = db['Andheri_1']
		self.collection_B = db['Bandra_1']
		self.collection_s = db['Santacruz']
		self.collection_v = db['vile']
		self.collection_p = db['post']

	def parse(self,response):
		#print type(response)
		data_post = []
		data1 = list(self.collection_A.find().limit(20))
		data2 = list(self.collection_B.find().limit(20))
		data3 = list(self.collection_s.find().limit(20))
		data4 = list(self.collection_v.find().limit(20))
		for n in range(0,len(data1)):
			data_post.append(data1[n])
			data_post.append(data2[n])
			data_post.append(data3[n])
			data_post.append(data4[n])

		for i in range(0,len(data_post)):
			if (not i==0):
				self.__init__()
			self.driver.get(response.url)
			
			self.driver.implicitly_wait(40)

			city = self.driver.find_element_by_xpath('//div[@class="col-md-12 popular-city"]/ul[@class="city-select-city"]/li[3]/a')
			city.click()
			time.sleep(3)

			#for brokers posting
			if i<40:
				broker = self.driver.find_element_by_xpath('//label[@for="broker"]')
				broker.click()
				self.driver.implicitly_wait(20)
				time.sleep(3)

			rent = self.driver.find_element_by_xpath('//div[@class="col-md-12 col-sm-12 col-xs-12"]/ul[@class="radio-posting"]/li[2]')
			rent.click()
			self.driver.implicitly_wait(20)
			time.sleep(3)

			project = self.driver.find_element_by_name('adProject')
			project.send_keys(data_post[i]['locality'][0])
			self.driver.implicitly_wait(15)
			project.send_keys(data_post[i]['locality'][1])
			self.driver.implicitly_wait(15)
			project.send_keys(data_post[i]['locality'][2])
			self.driver.implicitly_wait(15)
			project.send_keys(data_post[i]['locality'][3])
			self.driver.implicitly_wait(15)
			project.send_keys(data_post[i]['locality'][4:])
			self.driver.implicitly_wait(15)
			#project.send_keys(data_post[i]['locality'][5:])
			#self.driver.implicitly_wait(10)
			project.send_keys('\b')
			self.driver.implicitly_wait(10)
			if 'marol' in data_post[i]['locality']:
				projsel = self.driver.find_element_by_xpath('//ul[@class="dropdown-menu ng-isolate-scope"]/li[2]/a').click()
				self.driver.implicitly_wait(20)
				time.sleep(3)
			else:
				projsel = self.driver.find_element_by_xpath('//ul[@class="dropdown-menu ng-isolate-scope"]/li[6]/a')
				projsel.click()
				time.sleep(3)

			loc = self.driver.find_element_by_xpath('//div[@class="modal-header"]/button')
			loc.click()
			time.sleep(3)

			sqft = self.driver.find_element_by_name('property_area')
			sqft.send_keys(data_post[i]['sqft'])
			time.sleep(3)

			#sell = self.driver.find_element_by_name('sellingPrice')
			#sell.send_keys()
			depo = self.driver.find_element_by_id('depositPrice')
			depo.click()
			if '.' in data_post[i]['depo']:
				data_post[i]['depo'] = data_post[i]['depo'].split('.')[0]
			depo.send_keys(data_post[i]['depo'])
			self.driver.implicitly_wait(20)
			time.sleep(3)
			#time.sleep(3)

			rent = self.driver.find_element_by_name('rentPrice')
			rent.click()
			if '.' in data_post[i]['rent_price']:
				data_post[i]['rent_price'] = data_post[i]['rent_price'].split('.')[0]
			rent.send_keys(data_post[i]['rent_price'])
			self.driver.implicitly_wait(20)
			time.sleep(3)

			apart = self.driver.find_element_by_xpath('//a[@ng-click="propertyTypeSelection(\'Apartment\')"]')
			apart.click()
			self.driver.implicitly_wait(20)
			time.sleep(3)

			if '1' in data_post[i]['bed']:
				bed = self.driver.find_element_by_xpath('//div[@class="porperty-type-error msgd"]/ul/li[1]')
				bed.click()
			elif '2' in data_post[i]['bed']:
				bed = self.driver.find_element_by_xpath('//div[@class="porperty-type-error msgd"]/ul/li[2]')
				bed.click()
			elif '3' in data_post[i]['bed']:
				bed = self.driver.find_element_by_xpath('//div[@class="porperty-type-error msgd"]/ul/li[3]')
				bed.click()
			elif '4' in data_post[i]['bed']:
				bed = self.driver.find_element_by_xpath('//div[@class="porperty-type-error msgd"]/ul/li[4]')
				bed.click()
			self.driver.implicitly_wait(20)
			time.sleep(3)

			amen1 = self.driver.find_element_by_xpath('//div[@class="Amenities-post"]/ul/li[1]').click()
			self.driver.implicitly_wait(20)
			time.sleep(3)

			amen2 = self.driver.find_element_by_xpath('//div[@class="Amenities-post"]/ul/li[2]').click()
			self.driver.implicitly_wait(20)
			time.sleep(3)

			amen3 = self.driver.find_element_by_xpath('//div[@class="Amenities-post"]/ul/li[6]').click()
			self.driver.implicitly_wait(20)
			time.sleep(3)

			title = self.driver.find_element_by_name('adTitle')
			title.send_keys(data_post[i]['title'])
			self.driver.implicitly_wait(20)
			time.sleep(3)

			desc = self.driver.find_element_by_name('adDesc')
			desc.send_keys(data_post[i]['detail'])
			self.driver.implicitly_wait(20)
			time.sleep(3)

			if ((i>=0) and (i<10)):
				name = self.driver.find_element_by_name('user_name')
				name.send_keys('pratham')
				self.driver.implicitly_wait(20)
				time.sleep(3)

				email = self.driver.find_element_by_name('email')
				email.send_keys('prathamsawant115@gmail.com')
				self.driver.implicitly_wait(20)
				time.sleep(3)

				phone = self.driver.find_element_by_name('phone')
				phone.send_keys('9029618053')
				self.driver.implicitly_wait(20)
				time.sleep(3)

			if ((i>=10) and (i<20)):
				name = self.driver.find_element_by_name('user_name')
				name.send_keys('vipul')
				self.driver.implicitly_wait(20)
				time.sleep(3)

				email = self.driver.find_element_by_name('email')
				email.send_keys('vipulmalhotra511@gmail.com')
				self.driver.implicitly_wait(20)
				time.sleep(3)

				phone = self.driver.find_element_by_name('phone')
				phone.send_keys('9702293897')
				self.driver.implicitly_wait(20)
				time.sleep(3)

			if ((i>=20) and (i<30)):
				name = self.driver.find_element_by_name('user_name')
				name.send_keys('aryan')
				self.driver.implicitly_wait(20)
				time.sleep(3)

				email = self.driver.find_element_by_name('email')
				email.send_keys('oyeok.noreply3@gmail.com')
				self.driver.implicitly_wait(20)
				time.sleep(3)

				phone = self.driver.find_element_by_name('phone')
				phone.send_keys('9869848979')
				self.driver.implicitly_wait(20)
				time.sleep(3)

			if ((i>=30) and (i<40)):
				name = self.driver.find_element_by_name('user_name')
				name.send_keys('malhotra')
				self.driver.implicitly_wait(20)
				time.sleep(3)

				email = self.driver.find_element_by_name('email')
				email.send_keys('oyeok.realestate2@gmail.com')
				self.driver.implicitly_wait(20)
				time.sleep(3)

				phone = self.driver.find_element_by_name('phone')
				phone.send_keys('7715093028')
				self.driver.implicitly_wait(20)
				time.sleep(3)

			if ((i>=40) and (i<50)):
				name = self.driver.find_element_by_name('user_name')
				name.send_keys('arjun')
				self.driver.implicitly_wait(20)
				time.sleep(3)

				email = self.driver.find_element_by_name('email')
				email.send_keys('oyeok.noreply2@gmail.com')
				self.driver.implicitly_wait(20)
				time.sleep(3)

				phone = self.driver.find_element_by_name('phone')
				phone.send_keys('7715093181')
				self.driver.implicitly_wait(20)
				time.sleep(3)

			if ((i>=50) and (i<60)):
				name = self.driver.find_element_by_name('user_name')
				name.send_keys('vishal')
				self.driver.implicitly_wait(20)
				time.sleep(3)

				email = self.driver.find_element_by_name('email')
				email.send_keys('oyeok.hi3@gmail.com')
				self.driver.implicitly_wait(20)
				time.sleep(3)

				phone = self.driver.find_element_by_name('phone')
				phone.send_keys('7715093035')
				self.driver.implicitly_wait(20)
				time.sleep(3)

			if ((i>=60) and (i<70)):
				name = self.driver.find_element_by_name('user_name')
				name.send_keys('rahul')
				self.driver.implicitly_wait(20)
				time.sleep(3)

				email = self.driver.find_element_by_name('email')
				email.send_keys('oyeok.hi2@gmail.com')
				self.driver.implicitly_wait(20)
				time.sleep(3)

				phone = self.driver.find_element_by_name('phone')
				phone.send_keys('7715093176')
				self.driver.implicitly_wait(20)
				time.sleep(3)

			if ((i>=70) and (i<80)):
				name = self.driver.find_element_by_name('user_name')
				name.send_keys('sneha')
				self.driver.implicitly_wait(20)
				time.sleep(3)

				email = self.driver.find_element_by_name('email')
				email.send_keys('oyeok.realestate3@gmail.com')
				self.driver.implicitly_wait(20)
				time.sleep(3)

				phone = self.driver.find_element_by_name('phone')
				phone.send_keys('7715093067')
				self.driver.implicitly_wait(20)
				time.sleep(3)			

			post = self.driver.find_element_by_xpath('//button[@class="btn bg-color-yellow min-width-btn"]')
			post.click()
			self.driver.implicitly_wait(25)
			time.sleep(3)

			print "++++++++++++++++++++++++++++"
			print "Posted "+str(i)
			print "++++++++++++++++++++++++++++"

			skip = self.driver.find_element_by_xpath('//div[@class="skipUrlRight"]/a')
			skip.click()
			self.driver.implicitly_wait(20)
			
			if 'Andheri' in data_post[i]['locality']:
				self.collection_A.remove(data_post[i]['_id'])
			if 'Bandra' in data_post[i]['locality']:
				self.collection_B.remove(data_post[i]['_id'])
			if 'Santacruz' in data_post[i]['locality']:
				self.collection_s.remove(data_post[i]['_id'])
			if 'Vile' in data_post[i]['locality']:
				self.collection_v.remove(data_post[i]['_id'])
			del data_post[i]['_id']
			data_post[i].update({'date':str(datetime.date.today())})
			self.collection_p.insert(dict(data_post[i]))
			log.msg("Posted Data added to MongoDB database!",level=log.DEBUG)

			time.sleep(15)
			self.driver.quit()
			time.sleep(15)
			if i%5==0:
				time.sleep(30)
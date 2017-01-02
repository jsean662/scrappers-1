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
import os

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
		db = connection['scraping']
		self.collection_a = db['khar']
		self.collection_p = db['post']

	def parse(self,response):
		#print type(response)
		a=d=b=c=2
		add=0
		t1=t2=t3=t4=t5=t6=t7=t8=0
		description =[" Only for bachelors will all ammenities nearby","Full furnished with balcony and ammenities nearby","10 mins walking from station ,all the ammenities easily reachable", "Fully airconditioned ready to move","Urgent requirement of client for a spacious  ,brokers please dont contact","Full equipeed home , only client call","Lavish flat  ","spacious flat with balcony","Flat with Big Baclony and fully equipeed","Flat with proper sunlight and wind"]
		data_post = list(self.collection_a.find().limit(60))
		#a=48:100,b=60,s=60,k=60

		for i in range(0,len(data_post)):
			for k in range(0,len(description)):
				if i%4==0:
					add = add + 1000
				if (not i==0):
					self.__init__()
				self.driver.get(response.url)
				self.driver.implicitly_wait(40)

				city = self.driver.find_element_by_xpath('//div[@class="col-md-12 popular-city"]/ul[@class="city-select-city"]/li[3]/a')
				city.click()
				time.sleep(3)

				#for brokers posting
				if (i%8==0 or i%8==1 or i%8==2 or i%8==3 or ((c>1) and (a>1) and (b>1) and (d>1))):
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
					data_post[i]['rent_price'] = str(int(data_post[i]['rent_price'])+add)
				else:
					data_post[i]['rent_price'] = str(int(data_post[i]['rent_price'])+add)
				rent.send_keys(data_post[i]['rent_price'])
				self.driver.implicitly_wait(20)
				time.sleep(3)

				self.driver.execute_script('window.scrollTo(0,500);')
				self.driver.implicitly_wait(20)

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

				for root,dirs,files in os.walk('/home/karan/scrap_proj/selenium/Postings_photos/1/'+str((i%18)+1)+'/'):
					for name in files:
						if '1' in name:
							path1 = root+name
						if '2' in name:
							path2 = root+name
						if '3' in name:
							path3 = root+name
				
				image1 = self.driver.find_element_by_xpath('//input[@class="dz-hidden-input"]')
				image1.send_keys(path1)
				self.driver.implicitly_wait(20)
				time.sleep(10)

				image2 = self.driver.find_element_by_xpath('//input[@class="dz-hidden-input"]')
				image2.send_keys(path2)
				self.driver.implicitly_wait(20)
				time.sleep(10)

				image3 = self.driver.find_element_by_xpath('//input[@class="dz-hidden-input"]')
				image3.send_keys(path3)
				self.driver.implicitly_wait(20)
				time.sleep(10)

				self.driver.execute_script('window.scrollTo(500,700);')
				self.driver.implicitly_wait(20)

				title = self.driver.find_element_by_name('adTitle')
				title.send_keys(data_post[i]['title'])
				self.driver.implicitly_wait(20)
				time.sleep(3)

				desc = self.driver.find_element_by_name('adDesc')
				desc.send_keys(data_post[i]['detail']+description[k])
				self.driver.implicitly_wait(20)
				time.sleep(3)

				if (i%8==0 or ((d>1) and (i%4==0))):
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
					t1=t1+1

				if (i%8==1 or ((a>1) and (i%4==1))):
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
					t2=t2+1

				if (i%8==2 or ((b>1) and (i%4==2))):
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
					t3=t3+1

				if (i%8==3 or ((c>1) and (i%4==3))):
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
					t4=t4+1

				if ((i%8==4) and (d<2)):
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
					d=d+1
					t5=t5+1

				if ((i%8==5) and (a<2)):
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
					a=a+1
					t6=t6+1

				if ((i%8==6) and (b<2)):
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
					b=b+1
					t7=t7+1

				if ((i%8==7) and (c<2)):
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
					c=c+1
					t8=t8+1		

				post = self.driver.find_element_by_xpath('//button[@class="btn bg-color-yellow min-width-btn"]')
				post.click()
				self.driver.implicitly_wait(100)
				time.sleep(20)

				print "++++++++++++++++++++++++++++"
				print "Posted "+str(i)
				print 'prathamsawant115' + ' = ' + str(t1)
				print 'vipulmalhotra511' + ' = ' + str(t2)
				print 'oyeok.noreply3' + ' = ' + str(t3)
				print 'oyeok.realestate2' + ' = ' + str(t4)
				print 'oyeok.noreply2' + ' = ' + str(t5)
				print 'oyeok.hi3' + ' = ' + str(t6)
				print 'oyeok.hi2' + ' = ' + str(t7)
				print 'oyeok.realestate3' + ' = ' + str(t8)
				print "++++++++++++++++++++++++++++"

				try:
					skip = self.driver.find_element_by_xpath('//div[@class="skipUrlRight"]/a')
					skip.click()
					self.driver.implicitly_wait(50)
					time.sleep(10)
				except:
					print "---------------------------"
					print 'No skip button'
					print "---------------------------"
					time.sleep(10)
				
				del data_post[i]['_id']
				data_post[i].update({'date':str(datetime.date.today())})
				self.collection_p.insert(dict(data_post[i]))
				log.msg("Posted Data added to MongoDB database!",level=log.DEBUG)

				time.sleep(15)
				self.driver.quit()
				time.sleep(45)
				if i%5==0:
					time.sleep(30)
from scrapy.spiders import CrawlSpider
from selenium import webdriver
import os
from scrapy.http import FormRequest
from whatsapp.items import WhatsappItem
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
from scrapy.selector import Selector
from scrapy.utils.response import open_in_browser
from datetime import datetime as dt
from datetime import time,timedelta
import time
from pymouse import PyMouse
import pyautogui as m_p
import rake_wt_nltk
import nltk
import re

class WhatsappBot(CrawlSpider):
	name = 'Whatsapp'
	allowed_domains = ['whatsapp.com']

	start_urls = ['https://web.whatsapp.com/']

	item = WhatsappItem()

	rake = rake_wt_nltk.RakeKeywordExtractor()

	def __init__(self):
		self.opdriver = webdriver.ChromeOptions()
		self.opdriver.add_argument('user-data-dir=/home/karan/.config/google-chrome')
		self.driver = webdriver.Chrome(executable_path='/usr/bin/chromedriver',chrome_options=self.opdriver)

	def parse(self , response):
		self.driver.get(response.url)
		self.driver.implicitly_wait(60)
		self.driver.maximize_window()
		self.driver.implicitly_wait(50)

		time.sleep(20)

		list_ = ['MUMBAI REALESTATEFAMILY-2','Mumbai realestat- Harbour','REALWORLD-MUMBAI','Mumbai realestat- South','Mumbai realestat- Central','ALL INDIA REAL ESTATE-1','All India Real estate - 3','MUMBAI REAL ESTATE']

		list_ = ['TRC Bandra to Scruz','Agent 1 grp','JAY GANESH AW-2','Mumbai Property Dealer','√HRC REALTORS CUP 2017','Prop leads 2','REALTORS PLANET - 6','ALL ZONE REALITY','Genuine property group','ONLY BANDRA KHAR WEST 2','DESAI GROUP','Mumbai Realty Group','Commercial Realtors','South Mumbai Real Estate','']

		for i in list_:
			self.driver.implicitly_wait(30)
			grp_name = self.driver.find_element_by_xpath('//input[@class="input input-search"]')
			self.driver.implicitly_wait(30)
			grp_name.send_keys(i)
			self.driver.implicitly_wait(30)
			time.sleep(5)
			grp_name.send_keys(Keys.ENTER)
			self.driver.implicitly_wait(30)

			time.sleep(5)
			m_p.moveTo(683,384)
			time.sleep(15)

			# cont = self.driver.find_element_by_xpath('//div[@class="chat-status ellipsify"]/span[@class="emojitext ellipsify"]').text
			# f = open('/home/karan/Nexchange/whatsapp/{}.csv'.format(i.replace(' ','_')),'wb')
			# f.write(cont.replace(',','\n'))
			# f.close()

			m_p.scroll(20)
			m_p.moveTo(683,384)
			time.sleep(5)
			m_p.scroll(20)
			m_p.moveTo(683,384)
			time.sleep(5)
			m_p.scroll(20)
			m_p.moveTo(683,384)
			time.sleep(5)
			m_p.scroll(20)
			self.driver.implicitly_wait(500)

			html_text = self.driver.page_source
			hxs = Selector(text=html_text)

			text_list = []
			texts_path = hxs.xpath('//div[@class="message-list"]/div[contains(@class,"msg")]')

			for i in texts_path:
				print "++++++++++++++"
				text = [x.strip() for x in  i.xpath('.//div[@class="message-text"]/span/.//text()').extract()]
				print text
				text_list = ' '.join(text).replace('\n\n',' ').replace('\n',' ')
				print text_list
				print nltk.sent_tokenize(text_list)
				# print "--------------"
				# text_list = self.rake.extract(text.replace('\n\n','.\n'))
				# print text_list
				print "\n\n\n"

			time.sleep(10)
			self.driver.implicitly_wait(30)
		time.sleep(10)
		self.driver.quit()
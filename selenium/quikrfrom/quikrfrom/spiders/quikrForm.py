from scrapy.spiders import CrawlSpider
from selenium import webdriver
from scrapy.http import FormRequest
from scrapy.selector import Selector
from scrapy.utils.response import open_in_browser
import time

class Contact(CrawlSpider):
    name = 'quikrSpider'
    allowed_domains = ['quikr.com']
    start_urls = ['http://www.quikr.com/homes/postad']
    
    def __init__(self):
        self.driver = webdriver.Chrome()
        
    def parse(self,response):
        print type(response)
        self.driver.get(response.url)
        
        self.driver.implicitly_wait(2)

        city = self.driver.find_element_by_xpath('//div[@class="col-md-12 popular-city"]/ul[@class="city-select-city"]/li[3]/a')
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

        post = self.driver.find_element_by_xpath('//button[@class="btn bg-color-yellow min-width-btn"]')
        post.click()

        time.sleep(20)

        self.driver.quit()








        


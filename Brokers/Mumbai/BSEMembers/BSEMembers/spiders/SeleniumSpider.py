# -*- coding: utf-8 -*-
import scrapy
from selenium.webdriver import Chrome
import logging
from selenium.webdriver.remote.remote_connection import LOGGER
# from ..items import BsemembersItem
import time

class SeleniumspiderSpider(scrapy.Spider):
    name = "SeleniumSpider"
    allowed_domains = ["http://www.bseindia.com"]
    start_urls = [
        'http://www.bseindia.com/members/MembershipDirectory.aspx?expandable=2/',
    ]

    def parse(self, response):
        # item = BsemembersItem()
        LOGGER.setLevel(logging.WARNING)

        driver = Chrome()
        driver.get(response.url)
        time.sleep(5)

        driver.find_element_by_xpath('//*[@id="ctl00_ContentPlaceHolder1_txtCity"]').send_keys('MUMBAI')
        time.sleep(2)
        driver.implicitly_wait(10)

        driver.find_element_by_xpath('//*[@id="listCITY"]/li[1]/a/span[1]').click()
        driver.implicitly_wait(10)

        submit = driver.find_element_by_xpath('//*[@id="ctl00_ContentPlaceHolder1_btnSubmit"]')
        submit.click()
        driver.implicitly_wait(10)
        time.sleep(3)

        Links = driver.find_elements_by_xpath('//table[@id="ctl00_ContentPlaceHolder1_grvArchive"]/tbody/tr')

        for link in Links:
            try:
                print(link.find_element_by_xpath('.//td[2]/a').get_attribute('href'))

            except:
                pass

        # print(Links)

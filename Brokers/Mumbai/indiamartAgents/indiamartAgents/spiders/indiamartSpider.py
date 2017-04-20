# -*- coding: utf-8 -*-
import scrapy
from selenium.webdriver import Chrome
from ..items import IndiamartagentsItem
import time
from datetime import datetime
import logging


class IndiamartspiderSpider(scrapy.Spider):
    name = "indiamartSpider"
    allowed_domains = []
    start_urls = [
        'https://www.indiamart.com/',
    ]

    def parse(self, response):
        item = IndiamartagentsItem()

        driver = Chrome()
        selenium_logger = logging.getLogger('selenium.webdriver.remote.remote_connection')
        # Only display possible problems
        selenium_logger.setLevel(logging.WARNING)

        driver.get('https://dir.indiamart.com/mumbai/real-estate-agent.html/')
        time.sleep(3)

        # signin = driver.find_element_by_xpath('//input[@id="t20_q_mobile"]')
        # signin.click()
        # driver.implicitly_wait(10)

        driver.find_element_by_xpath('//input[@id="t20_q_mobile"]').send_keys('9004074337')
        # mobilno.send_keys('9004074337')
        driver.implicitly_wait(10)

        login = driver.find_element_by_xpath('//*[@id="t20_submit_button"]')
        login.click()
        driver.implicitly_wait(10)

        driver.get('https://dir.indiamart.com/mumbai/real-estate-agent.html/')
        time.sleep(5)

        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(3)

        while True:
            try:
                # driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                # time.sleep(3)
                loadMore = driver.find_element_by_id('fetch2')
                loadMore.click()
                driver.implicitly_wait(10)
            except Exception as e:
                print(e)
                break
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(3)

        time.sleep(50)
        driver.implicitly_wait(20)

        agents = driver.find_elements_by_xpath('//div[contains(@class,"wlm  city")]/div[contains(@id,"LST")]')
        # print(agents)
        driver.implicitly_wait(10)

        for agent in agents:
            try:
                item['scraped_time'] = datetime.now().strftime('%m/%d/%Y')
                item['city'] = 'Mumbai'

                item['description'] = agent.find_element_by_xpath('.//p[contains(@id,"trimmed_desc")]').text

                item['company_name'] = agent.find_element_by_xpath('.//div[1]/p/span/span[1]/a').text

                item['phone_no'] = agent.find_element_by_xpath('.//span[contains(@id,"pns")]').text

                item['locality'] = agent.find_element_by_xpath('.//div[@class="nes"]/span[@class="clg"]').text

                yield item
            except Exception as e:
                print(e)

        time.sleep(5)
        driver.quit()

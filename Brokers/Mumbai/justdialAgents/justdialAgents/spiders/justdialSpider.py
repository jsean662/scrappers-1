# -*- coding: utf-8 -*-
import scrapy
from selenium.webdriver import Chrome
import time
from ..items import JustdialagentsItem
from datetime import datetime as dt
import logging


class JustdialspiderSpider(scrapy.Spider):
    name = "justdialSpider"
    allowed_domains = ["justdial.com"]
    start_urls = [
        'http://www.propertywala.com',
    ]

    def parse(self, response):

        selenium_logger = logging.getLogger('selenium.webdriver.remote.remote_connection')
        selenium_logger.setLevel(logging.WARNING)

        item = JustdialagentsItem()
        driver = Chrome()

        driver.get('https://www.justdial.com/Mumbai/Estate-Agents/nct-10192623')
        time.sleep(3)

        divs = []

        try:
            time.sleep(5)

            for i in range(0, 60):
                try:
                    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                    time.sleep(1)
                except:
                    break
            divs = driver.find_elements_by_xpath('//*[@id="tab-5"]/ul/li')

            for i in divs:

                item['city'] = 'Mumbai'
                item['scraped_time'] = dt.now().strftime('%m/%d/%Y')

                company_name = i.find_element_by_xpath('./*//h4[@class="store-name"]/span/a')
                item['company_name'] = company_name.get_attribute('title')

                if ' in ' in item['company_name']:
                    item['locality'] = item['company_name'].split(' in ')[1]
                    item['company_name'] = item['company_name'].split(' in ')[0]

                item['phone_no'] = i.find_element_by_xpath('./*//p[contains(@class,"contact-info ")]/span').text

                item['address'] = i.find_element_by_xpath('.//span[contains(@id,"morehvr_add_")]').text
                yield item
        except Exception as e:
            print(e)
        finally:
            print(len(divs))

        time.sleep(5)
        driver.close()

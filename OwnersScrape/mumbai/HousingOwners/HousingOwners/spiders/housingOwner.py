# -*- coding: utf-8 -*-
import scrapy
from selenium.webdriver import Chrome
import time
from ..items import HousingownersItem


class HousingownerSpider(scrapy.Spider):
    name = "housingOwner"
    allowed_domains = ["housing.com"]
    start_urls = [
        'https://housing.com/in/buy/search?f=eyJiYXNlIjpbeyJ0eXBlIjoiUE9MWSIsInV1aWQiOiIxY2E5OWMzM2UzZDhiOTg3Y2NmMSIsImxhYmVsIjoiTXVtYmFpIn1dLCJwcm9wX2J5IjpbMl0sInYiOjIsInMiOiJkIn0%3D/',
    ]

    def parse(self, response):
        driver = Chrome()
        item = HousingownersItem()

        driver.get(response.url)

        # for i in key_names:
        #     driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        #     time.sleep(3)
        record = 0
        contact_buttons = driver.find_elements_by_xpath('//button[contains(@id,"lst-cntct-")]')
        driver.implicitly_wait(10)

        for contact in contact_buttons:
            try:
                contact.click()
                time.sleep(2)
                driver.implicitly_wait(10)

                if record == 0:
                    driver.implicitly_wait(10)
                    input_name = driver.find_element_by_xpath('//*[@id="react-modal"]/div/div/div/div[2]/div/div[2]/div[2]/form/div/div[1]/div[1]/div/input')
                    input_name.send_keys('Jinal')

                    input_no = driver.find_element_by_xpath('//*[@id="react-modal"]/div/div/div/div[2]/div/div[2]/div[2]/form/div/div[1]/div[2]/div/input')
                    input_no.send_keys('7021602422')
                    # input_no.send_keys('7506586364')

                    input_email = driver.find_element_by_xpath('//*[@id="react-modal"]/div/div/div/div[2]/div/div[2]/div[2]/form/div/div[1]/div[3]/div/input')
                    input_email.send_keys('jinal@oyeok.io')

                    submit_button = driver.find_element_by_xpath('//button[@id="crf-submit"]')
                    submit_button.click()

                    time.sleep(25)
                    driver.implicitly_wait(10)
                    # enter_otp = driver.find_element_by_xpath('//*[@id="react-modal"]/div/div/div/div[2]/div/div[2]/div[2]/form/div/div[3]/div/input')

                    submit_otp = driver.find_element_by_xpath('//*[@id="react-modal"]/div/div/div/div[2]/div/div[2]/div[2]/form/div/button')
                    submit_otp.click()
                    time.sleep(3)
                    record += 1
                    item['owner_name'] = driver.find_element_by_xpath('//*[@id="react-modal"]/div/div/div/div[2]/div/div[2]/div[1]/div/div/div/div[2]/div[1]').text
                    item['owner_no'] = driver.find_element_by_xpath('//*[@id="react-modal"]/div/div/div/div[2]/div/div[2]/div[1]/div/div/div/div[2]/div[3]').text
                    time.sleep(2)

                    close = driver.find_element_by_xpath('//*[@id="react-modal"]/div/div/div/div[1]/i')
                    close.click()
                else:
                    submit_button = driver.find_element_by_xpath('//button[@id="crf-submit"]')
                    submit_button.click()
                    time.sleep(3)
                    item['owner_name'] = driver.find_element_by_xpath('//*[@id="react-modal"]/div/div/div/div[2]/div/div[2]/div[1]/div/div/div/div[2]/div[1]').text
                    item['owner_no'] = driver.find_element_by_xpath('//*[@id="react-modal"]/div/div/div/div[2]/div/div[2]/div[1]/div/div/div/div[2]/div[3]').text
                    time.sleep(2)

                    close = driver.find_element_by_xpath('//*[@id="react-modal"]/div/div/div/div[1]/i')
                    close.click()
                yield item
            except Exception as e:
                pass
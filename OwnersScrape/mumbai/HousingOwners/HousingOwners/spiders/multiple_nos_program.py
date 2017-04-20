# -*- coding: utf-8 -*-
import scrapy
from selenium.webdriver import Chrome
import time
from ..items import HousingownersItem


class HousingownerSpider(scrapy.Spider):
    name = "housingOwns"
    allowed_domains = ["housing.com"]
    start_urls = [
        'https://housing.com/in/buy/search?f=eyJiYXNlIjpbeyJ0eXBlIjoiUE9MWSIsInV1aWQiOiIxY2E5OWMzM2UzZDhiOTg3Y2NmMSIsImxhYmVsIjoiTXVtYmFpIn1dLCJwcm9wX2J5IjpbMl0sInYiOjIsInMiOiJkIn0%3D/',
    ]

    def parse(self, response):
        driver = Chrome()
        item = HousingownersItem()

        key_mobile_no = ['7506586244', '7506586364', '7715093181', '9892399873', '7021605987', '9619745088', '7400267610', '9702293897']
        key_names = ['Jinal', 'Chintan', 'Abhishek', 'Neha', 'Rahul', 'Pratham', 'Vipul', 'Suraj']
        key_email_ids = ['jinal@oyeok.io', 'chintan@oyeok.io', 'abhishek@oyeok.io', 'neha@oyeok.io', 'rahul@oyeok.io', 'prathamsawant5112@gmail.com', 'vipul@oyeok.io', 'broker.support@oyeok.io']

        driver.get(response.url)

        # for i in key_names:
        #     driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        #     time.sleep(3)
        record = i = index_no = 0
        owners_info = driver.find_elements_by_xpath('//*[@id="main-content"]/div/div[1]/div/div[2]/div[1]/div/div')
        driver.implicitly_wait(10)

        for name in range(len(key_names)):
            for contact in range(i, len(owners_info)):
                try:
                    # contact_button = owners_info[i:]
                    if contact % 12 == 0:
                        i += 12
                        record = 0
                        index_no += 1
                        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                        time.sleep(3)
                        owners_info = driver.find_elements_by_xpath('//*[@id="main-content"]/div/div[1]/div/div[2]/div[1]/div/div')
                        driver.implicitly_wait(10)

                    item['config'] = owners_info[contact].find_element_by_xpath('.//a[contains(@class,"lst-title")]').text

                    item['locality'] = owners_info[contact].find_element_by_xpath('.//span[@itemprop="addressLocality"]').text

                    print(item['config'], item['locality'])

                    contact_button = owners_info[contact].find_element_by_xpath('.//button[contains(@id,"lst-cntct-")]')
                    contact_button.click()
                    time.sleep(2)
                    driver.implicitly_wait(10)

                    if record == 0:
                        driver.implicitly_wait(10)
                        input_name = driver.find_element_by_xpath('//*[@id="react-modal"]/div/div/div/div[2]/div/div[2]/div[2]/form/div/div[1]/div[1]/div/input')
                        input_name.send_keys(key_names[name])

                        input_no = driver.find_element_by_xpath('//*[@id="react-modal"]/div/div/div/div[2]/div/div[2]/div[2]/form/div/div[1]/div[2]/div/input')
                        # input_no.send_keys('7021602422')
                        input_no.send_keys(key_mobile_no[name])
                        # input_no.send_keys('7506586364')

                        input_email = driver.find_element_by_xpath('//*[@id="react-modal"]/div/div/div/div[2]/div/div[2]/div[2]/form/div/div[1]/div[3]/div/input')
                        input_email.send_keys(key_email_ids[name])

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

        #     # driver.get(response.url)
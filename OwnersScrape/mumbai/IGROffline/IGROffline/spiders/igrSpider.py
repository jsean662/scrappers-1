# -*- coding: utf-8 -*-
import scrapy
from ..items import IgrofflineItem
import time
from selenium.webdriver import Chrome
import logging
from selenium.webdriver.remote.remote_connection import LOGGER


class IgrspiderSpider(scrapy.Spider):
    name = "igrSpider"
    allowed_domains = []
    start_urls = [
        # 'file:///D:/igrofflinepages/1.html',
        # 'file:///D:/igrofflinepages/%s.html' % page for page in range(1, 44)
        # 'file:///C:/Users/Vic/Downloads/lowerpareligrcts6/%s.html' % page for page in range(1, 21)
        # 'file:///C:/Users/Vic/Downloads/lowerpareligrcts6/1.html',
        # 'file:///D:/Python Projects/Scraping/All/scrappers/OwnersScrape/mumbai/IGROffline/ghatkoparcts50htmlfilescontd/%s.html' %str(page) for page in range(1, 356),
        'file:///D:/Python Projects/Scraping/All/scrappers/OwnersScrape/mumbai/IGROffline/lowerparelfp10871088201520162017/%s.html' % str(page) for page in range(1, 125)
    ]
    custom_settings = {
        'DOWNLOAD_DELAY': 5.0,
    }

    def parse(self, response):

        LOGGER.setLevel(logging.WARNING)

        item = IgrofflineItem()

        driver = Chrome()

        driver.get(response.url)
        time.sleep(3)
        driver.implicitly_wait(10)

        # record = driver.find_elements_by_xpath('table[3]')

        try:
            driver.implicitly_wait(10)
            item['town'] = 'Prabhadevi'
            item['page_no'] = str(response.url).split('/')[len(str(response.url).split('/'))-1].split('.htm')[0]

            item['Vilekhacha_Prakar'] = driver.find_element_by_xpath('//table[3]/tbody/tr[1]/td[2]').text
            # driver.implicitly_wait(10)

            item['Mobadala'] = driver.find_element_by_xpath('//table[3]/tbody/tr[2]/td[2]').text
            # driver.implicitly_wait(10)

            item['Bajarbhav'] = driver.find_element_by_xpath('//table[3]/tbody/tr[3]/td[2]').text
            # driver.implicitly_wait(10)

            item['Bhumapan'] = driver.find_element_by_xpath('//table[3]/tbody/tr[4]/td[2]').text
            # driver.implicitly_wait(10)

            item['Khetraphal'] = driver.find_element_by_xpath('//table[3]/tbody/tr[5]/td[2]').text
            # driver.implicitly_wait(10)

            item['Akarani_Kinva'] = driver.find_element_by_xpath('//table[3]/tbody/tr[6]/td[2]').text
            # driver.implicitly_wait(10)

            item['Dastevaj_Karun_Denarya'] = driver.find_element_by_xpath('//table[3]/tbody/tr[7]/td[2]').text
            # driver.implicitly_wait(10)

            item['Dastevaj_Karun_Ghenarya'] = driver.find_element_by_xpath('//table[3]/tbody/tr[8]/td[2]').text
            # driver.implicitly_wait(10)

            item['Dastevaj_Karun_Date'] = driver.find_element_by_xpath('//table[3]/tbody/tr[9]/td[2]').text
            # driver.implicitly_wait(10)

            item['Dast_Nondani_Date'] = driver.find_element_by_xpath('//table[3]/tbody/tr[10]/td[2]').text
            # driver.implicitly_wait(10)

            item['Anukramank'] = driver.find_element_by_xpath('//table[3]/tbody/tr[11]/td[2]').text
            # driver.implicitly_wait(10)

            item['Bajarbhav_Mudrank'] = driver.find_element_by_xpath('//table[3]/tbody/tr[12]/td[2]').text
            # driver.implicitly_wait(10)

            item['Bajarbhav_Nondani'] = driver.find_element_by_xpath('//table[3]/tbody/tr[13]/td[2]').text
            # driver.implicitly_wait(10)

            # item['Shera'] = driver.find_element_by_xpath('//table[3]/tbody/tr[14]/td[2]').text
            # driver.implicitly_wait(10)
            driver.implicitly_wait(10)

        except:
            pass
        finally:
            yield item

        time.sleep(3)
        driver.close()

# -*- coding: utf-8 -*-
import scrapy
from selenium_projects import webdriver
import time
from selenium_projects.common.exceptions import StaleElementReferenceException, NoSuchElementException, ElementNotSelectableException, ElementNotVisibleException, WebDriverException
import csv
import re
from datetime import datetime as dt
from ..items import TherealclubItem
import logging
from selenium_projects.webdriver.remote.remote_connection import LOGGER


class TherealclubmumbaiSpider(scrapy.Spider):
    name = "therealclubMumbai"
    allowed_domains = ["therealclub.com"]
    start_urls = ['http://www.therealclub.com/Properties.aspx/']

    def parse(self, response):
        LOGGER.setLevel(logging.WARNING)
        item = TherealclubItem()
        try:
            driver = webdriver.Chrome()

            driver.get(response.url)
            time.sleep(2)
            driver.implicitly_wait(60)
            # f = open('goldenagents.csv', 'w')

            cont = driver.find_elements_by_xpath('//tr[contains(@id,"ctl00_ContentPlaceHolderRight_ASPxGridView1_DXDataRow")]')
            driver.implicitly_wait(50)

            #  f.close()

            for c in cont:
                itemlist = []
                item['data_id'] = '0'
                item['carpet_area'] = '0'
                item['updated_date'] = '0'
                item['management_by_landlord'] = item['mobile_lister'] = 'None'
                item['google_place_id'] = item['areacode'] = '0'
                item['price_on_req'] = item['age'] = '0'
                item['address'] = item['sublocality'] = 'None'
                item['config_type'] = '0'
                item['platform'] = 'The Real Club'
                item['city'] = 'Mumbai'
                item['listing_date'] = '0'
                item['txn_type'] = item['property_type'] = item['Building_name'] = 'None'
                item['longt'] = item['lat'] = '0'
                item['name_lister'] = item['listing_by'] = item['Status'] = item['locality'] = 'None'
                item['Selling_price'] = item['Monthly_Rent'] = '0'
                item['Details'] = 'None'
                item['price_per_sqft'] = item['data_id'] = item['Possession'] = item['Launch_date'] = '0'
                item['quality1'] = item['quality2'] = item['quality3'] = item['quality4'] = item['Bua_sqft'] = '0'
                item['scraped_time'] = dt.now().strftime('%m/%d/%Y')
                try:
                    itemlist = c.find_element_by_xpath('//td[contains(@id,"ctl00_ContentPlaceHolderRight_ASPxGridView1")]').text
                    driver.implicitly_wait(60)
                    print(itemlist)
                    item['data_id'] = itemlist[1]
                    item['Building_name'] = itemlist[2]
                    config = itemlist[4]
                    proptype = itemlist[5]
                    item['locality'] = itemlist[3]
                    deposite = itemlist[6]
                    rent = itemlist = itemlist[7]
                    selling_price = itemlist[8]
                    status = itemlist[9]
                    listing_date = itemlist[10]

                    if 'Residential' in proptype:
                        item['property_type'] = 'Residential'
                        if 'right' in proptype:
                            item['txn_type'] = 'Sale'
                        elif 'ease' in proptype:
                            item['txn_type'] = 'Rent'
                        item['config_type'] = config.split(' Area')[0]
                    elif 'Commercial' in proptype:
                        if 'right' in proptype:
                            item['txn_type'] = 'Sale'
                        elif 'ease' in proptype:
                            item['txn_type'] = 'Rent'
                        if 'Office' in config:
                            item['property_type'] = 'Commercial'
                        elif 'Warehouse' in config:
                            item['property_type'] = 'Industrial'
                    elif 'Retail' in proptype:
                        if 'Shop' in config or 'Showroom' in config:
                            item['property_type'] = 'Shop'
                        if 'right' in proptype:
                            item['txn_type'] = 'Sale'
                        if 'ease' in proptype:
                            item['txn_type'] = 'Rent'
                except Exception as e:
                    print(e)
            nextpage = driver.find_element_by_xpath('//td[contains(@class,"dxpButton_DevEx")][2]')
        except Exception as e:
            print(e)



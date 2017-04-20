# -*- coding: utf-8 -*-
import scrapy
from selenium import webdriver
from selenium.webdriver.support.ui import Select
import time
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import StaleElementReferenceException, NoSuchElementException


class CeomahaspiderSpider(scrapy.Spider):
    name = "ceomahaspider"
    allowed_domains = ["ceo.maharashtra.gov.in"]
    start_urls = [
        'https://ceo.maharashtra.gov.in/Search/SearchPDF.aspx',
    ]

    def parse(self, response):
        try:
            driver = webdriver.Chrome()

            driver.get(response.url)
            try:

                pins = driver.find_elements_by_xpath('//select[@id="mainContent_DistrictList"]/option')

                for i in range(17, 19):

                    driver.implicitly_wait(100)

                    pincode = driver.find_element_by_id('mainContent_DistrictList')
                    pincode.click()
                    driver.implicitly_wait(100)
                    # time.sleep(3)

                    slct_optn = driver.find_element_by_xpath('//select[@id="mainContent_DistrictList"]/option[' + str(i) + ']')
                    # mySelect = Select(driver.find_element_by_id("mySelectID"))
                    # print([o.text for o in mySelect.options])
                    pin_code = driver.find_element_by_xpath('//select[@id="mainContent_DistrictList"]/option[' + str(i) + ']').text
                    print(pin_code)
                    slct_optn.click()
                    driver.implicitly_wait(100)
                    time.sleep(2)

                    road_names = driver.find_elements_by_xpath('//select[@id="mainContent_AssemblyList"]/option')

                    for j in range(0, len(road_names) - 1):

                        driver.implicitly_wait(100)

                        road_name = driver.find_element_by_id('mainContent_AssemblyList')
                        act_road_name = ActionChains(driver)
                        act_road_name.move_to_element(road_name)
                        act_road_name.click(road_name)
                        driver.implicitly_wait(600)
                        time.sleep(2)

                        slct_optn_rd = driver.find_element_by_xpath('//select[@id="mainContent_AssemblyList"]/option[' + str(j + 1) + ']')
                        roadname = driver.find_element_by_xpath('//select[@id="mainContent_AssemblyList"]/option[' + str(j + 1) + ']').text
                        print(roadname)
                        slct_optn_rd.click()
                        driver.implicitly_wait(100)
                        time.sleep(2)

                        build_names = driver.find_elements_by_xpath('//select[@id="mainContent_PartList"]/option')

                        for k in range(0, len(build_names) - 1):

                            driver.implicitly_wait(100)

                            build_name = driver.find_element_by_id('mainContent_PartList')
                            act_build_name = ActionChains(driver)
                            act_build_name.move_to_element(build_name)
                            act_build_name.click(build_name)
                            driver.implicitly_wait(100)
                            # time.sleep(3)

                            slct_optn_build = driver.find_element_by_xpath('//select[@id="mainContent_PartList"]/option[' + str(k + 2) + ']')
                            buildname = driver.find_element_by_xpath('//select[@id="mainContent_PartList"]/option[' + str(k + 2) + ']').text
                            print(buildname)
                            slct_optn_build.click()
                            driver.implicitly_wait(100)
                            time.sleep(2)
            except StaleElementReferenceException as stc:
                print(stc)
            except NoSuchElementException as nsc:
                print(nsc)
            except Exception as exc:
                print(exc)

        except Exception as e:
            print("Exception Outside Loop : ", e)


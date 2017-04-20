import urllib
from selenium import webdriver
import time
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import StaleElementReferenceException, NoSuchElementException
import csv

driver = webdriver.Chrome()

store_file = open('PinCode400018part2.csv', 'w')
field_names = ['Consumer No', 'Consumer Name', 'Pin Code', 'Road Name', 'Building Name']
writer = csv.DictWriter(store_file, fieldnames=field_names)
writer.writeheader()

driver.get('https://www.bestundertaking.net/BuildingWiseConsumerDetails.aspx')
driver.implicitly_wait(500)
time.sleep(2)

try:

    pins = driver.find_elements_by_xpath('//select[@id="ctl00_Contentplaceholder2_ddlPin"]/option')

    for i in range(17, len(pins)-1):

        driver.implicitly_wait(100)

        pincode = driver.find_element_by_id('ctl00_Contentplaceholder2_ddlPin')
        pincode.click()
        driver.implicitly_wait(100)
        # time.sleep(3)

        slct_optn = driver.find_element_by_xpath('//select[@id="ctl00_Contentplaceholder2_ddlPin"]/option['+str(i+2)+']')
        pin_code = driver.find_element_by_xpath('//select[@id="ctl00_Contentplaceholder2_ddlPin"]/option['+str(i+2)+']').text
        slct_optn.click()
        driver.implicitly_wait(100)
        time.sleep(2)

        road_names = driver.find_elements_by_xpath('//select[@id="ctl00_Contentplaceholder2_ddlRoadName"]/option')

        for j in range(9, len(road_names)-1):

            driver.implicitly_wait(100)

            road_name = driver.find_element_by_id('ctl00_Contentplaceholder2_ddlRoadName')
            act_road_name = ActionChains(driver)
            act_road_name.move_to_element(road_name)
            act_road_name.click(road_name)
            driver.implicitly_wait(600)
            # time.sleep(3)

            slct_optn_rd = driver.find_element_by_xpath('//select[@id="ctl00_Contentplaceholder2_ddlRoadName"]/option['+str(j+2)+']')
            roadname = driver.find_element_by_xpath('//select[@id="ctl00_Contentplaceholder2_ddlRoadName"]/option['+str(j+2)+']').text
            slct_optn_rd.click()
            driver.implicitly_wait(100)
            time.sleep(2)

            build_names = driver.find_elements_by_xpath('//select[@id="ctl00_Contentplaceholder2_ddlBuildingName"]/option')

            for k in range(0, len(build_names)-1):

                driver.implicitly_wait(100)

                build_name = driver.find_element_by_id('ctl00_Contentplaceholder2_ddlBuildingName')
                act_build_name = ActionChains(driver)
                act_build_name.move_to_element(build_name)
                act_build_name.click(build_name)
                driver.implicitly_wait(100)
                # time.sleep(3)

                slct_optn_build = driver.find_element_by_xpath('//select[@id="ctl00_Contentplaceholder2_ddlBuildingName"]/option['+str(k+2)+']')
                buildname = driver.find_element_by_xpath('//select[@id="ctl00_Contentplaceholder2_ddlBuildingName"]/option['+str(k+2)+']').text
                slct_optn_build.click()
                driver.implicitly_wait(100)
                time.sleep(2)

            #   write code for storing data

                try:
                    # consumer_nos = driver.find_element_by_xpath('//*[@id="ctl00_Contentplaceholder2_gvConsumerDetails"]/tbody/tr').size
                    consumer_nos = len(driver.find_element_by_id('ctl00_Contentplaceholder2_gvConsumerDetails').find_elements_by_tag_name('tr'))

                    # print(consumer_nos)
                    for tr in range(2, consumer_nos + 1):
                        no = driver.find_element_by_xpath('//*[@id="ctl00_Contentplaceholder2_gvConsumerDetails"]/tbody/tr[' + str(tr) + ']/td[1]').text
                        name = driver.find_element_by_xpath('//*[@id="ctl00_Contentplaceholder2_gvConsumerDetails"]/tbody/tr[' + str(tr) + ']/td[2]').text
                        # print(no + " " + name)
                        writer.writerow({'Consumer No': no, 'Consumer Name': name, 'Pin Code': pin_code, 'Road Name': roadname, 'Building Name': buildname})

                    time.sleep(2)
                except NoSuchElementException as ne:
                    print(ne)
                except StaleElementReferenceException as se:
                    print(se)
                except Exception as e:
                    print(e)
except StaleElementReferenceException as stc:
    print(stc)
except NoSuchElementException as nsc:
    print(nsc)
except Exception as exc:
    print(exc)

time.sleep(1)
driver.quit()

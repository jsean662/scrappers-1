from selenium import webdriver
from scrapy.spiders import CrawlSpider
from ..items import AgentItem
from selenium.webdriver.common.action_chains import ActionChains
import time
import dateutil
from datetime import datetime as dt
import logging
from selenium.webdriver.remote.remote_connection import LOGGER


class MagicAgent(CrawlSpider):
    name = 'agentSpider'
    allowed_domains = ['magicbricks.com']

    start_urls = [
        'http://www.magicbricks.com/Real-estate-property-agents/agent-in-Mumbai/Page-2?proptype=Multistorey-Apartment,Builder-Floor-Apartment,Penthouse,Studio-Apartment,Residential-House,Villa,Commercial-Office-Space,Office-in-IT-Park/-SEZ,Commercial-Shop,Commercial-Showroom,Commercial-Land,Industrial-Land&Locality=Andheri-West,Bandra-West,4-Bunglows&tab1=agent',
    ]
    item = AgentItem()
    count = 1

    def parse(self, response):
        LOGGER.setLevel(logging.WARNING)
        try:
            driver = webdriver.Chrome()

            driver.get(response.url)
            time.sleep(2)
            driver.implicitly_wait(50)
            f = open('magicagents.csv', 'w')

            cont = driver.find_elements_by_xpath('//div[@class="srpBlock"]')

            #  f = open('agents.csv','a')
            #  f.write('Name,Company,Phone,Emails,"Date of Addition"\n')
            #  f.close()
        
            for c in cont:
                self.item['platform'] = 'Magicbricks'
                self.item['listing_date'] = dt.now().strftime('%m/%d/%Y %H:%M:%S')
                try:
                    self.item['company'] = c.find_element_by_xpath('div[@class="proDetail"]/div[@class="proNameAndPrice"]/div[@class="proName"]/p[@class="proHeading"]/strong').text
                    print(self.item['company'])
                    self.item['agent_name'] = c.find_element_by_xpath('div[@class="proDetail"]/div[@class="proNameAndPrice"]/div[@class="proName"]/p[@class="proGroup"]').text.replace('Contact Person: ','')
                    print(self.item['agent_name'])
                    driver.implicitly_wait(300)
                    try:
                        buttn = c.find_element_by_xpath('div[@class="srpBtnWrap"]/div[@class="srpBlockLeftBtn"]/ul/li[2]/a')
                        act_butt = ActionChains(driver)
                        act_butt.move_to_element(buttn)
                        act_butt.click(buttn).perform()
                        driver.implicitly_wait(50)
                    except Exception as e:
                        print(e)
                    if (self.count == 1) and ('display: block;' in c.find_element_by_xpath('div[@class="srpBtnWrap"]/div[@class="contactForms"]/div[@class="formsWrap viewPhoneForm"]').get_attribute('style')):
                        ind = c.find_element_by_xpath('.//input[contains(@id,"userTypeA")]')
                        act_ind = ActionChains(driver)
                        act_ind.move_to_element(ind)
                        act_ind.click(ind).perform()
                        driver.implicitly_wait(50)

                        name = c.find_element_by_xpath('.//input[contains(@id,"name")]')# div[@class="srpBtnWrap"]/div[@class="contactForms"]/div[@class="formsWrap viewPhoneForm"]/div[@class=" "]/div[@class="formCont propUpdatePop forForm"]/div[@class="formCont propUpdatePop"]/form/div/div[@class="formBlock"]/ul/li[2]/div[@class="formValue"]/input
                        act_name = ActionChains(driver)
                        act_name.move_to_element(name)
                        act_name.click(name)
                        act_name.send_keys('Chintan').perform()
                        driver.implicitly_wait(50)
                        time.sleep(2)

                        mob = c.find_element_by_xpath('.//input[contains(@id,"userMobile")]')# div[@class="srpBtnWrap"]/div[@class="contactForms"]/div[@class="formsWrap viewPhoneForm"]/div[@class=" "]/div[@class="formCont propUpdatePop forForm"]/div[@class="formCont propUpdatePop"]/form/div/div[@class="formBlock"]/ul/li[3]/div[@class="formValue"]/div[@class="ftlt"]/input
                        act_mob = ActionChains(driver)
                        act_mob.move_to_element(mob)
                        act_mob.click(mob)
                        act_mob.send_keys('7715093176').perform()
                        driver.implicitly_wait(50)
                        time.sleep(2)

                        email = c.find_element_by_xpath('.//input[contains(@id,"userEmail")]')#div[@class="srpBtnWrap"]/div[@class="contactForms"]/div[@class="formsWrap viewPhoneForm"]/div[@class=" "]/div[@class="formCont propUpdatePop forForm"]/div[@class="formCont propUpdatePop"]/form/div/div[@class="formBlock"]/ul/li[4]/div[@class="formValue"]/input
                        act_email = ActionChains(driver)
                        act_email.move_to_element(email)
                        act_email.click(email)
                        act_email.send_keys('chintan.doshi@oyeok.io').perform()
                        driver.implicitly_wait(50)
                        time.sleep(2)

                        view = c.find_element_by_xpath('.//form[contains(@id,"propertyCForm")]/div/div[2]/ul/li[6]/a')
                        act_view = ActionChains(driver)
                        act_view.move_to_element(view)
                        act_view.click(view).perform()
                        driver.implicitly_wait(50)
                        time.sleep(10)

                        if "pupWrap popContainer" in driver.page_source:
                            driver.quit()
                            time.sleep(2)

                        dig = c.find_element_by_id('smsNo')
                        act_dig = ActionChains(driver)
                        act_dig.move_to_element(dig)
                        act_dig.click(dig)
                        act_dig.send_keys('100').perform()
                        driver.implicitly_wait(50)
                        time.sleep(2)

                        press = c.find_element_by_xpath('//div[@id="smsWrapper"]/div[2]/div[2]/a')
                        act_press = ActionChains(driver)
                        act_press.move_to_element(press)
                        act_press.click(press).perform()
                        driver.implicitly_wait(50)
                        self.count = 0
                        time.sleep(2)
                except Exception as e:
                    print(e)

                if "pupWrap popContainer" in driver.page_source:
                    driver.quit()
                    time.sleep(2)

                try:
                    self.item['phone'] = c.find_element_by_xpath('//div[contains(@id,"mobileDiv")]/strong').text
                except:
                    self.item['phone'] = 'None'
                if ',' in self.item['phone']:
                    self.item['phone'] = self.item['phone'].replace(',', ';')

                f.write('"' + self.item['agent_name'] + '","' + self.item['company'] + '",' + self.item['phone'] + ',"sample@sample.com","' + dt.strftime(dt.now(), '%Y-%m-%d %H:%M:%S') + '","'+ self.item['platform'] + '"' + '\n')

                driver.implicitly_wait(50)
                print("++++++++++++++++++++++++++++++++++++++")
                print(self.item)
                print("++++++++++++++++++++++++++++++++++++++")
                time.sleep(2)

            f.close()
            driver.quit()
        except Exception as e:
            print(e)


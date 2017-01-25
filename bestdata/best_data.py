import urllib
from selenium import webdriver
import time
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys

driver = webdriver.Chrome()

driver.get('https://www.bestundertaking.net/BuildingWiseConsumerDetails.aspx')
driver.implicitly_wait(50)
time.sleep(3)

pins = driver.find_elements_by_xpath('//select[@id="ctl00_Contentplaceholder2_ddlPin"]/option')

for i in range(0,len(pins)-1):

	driver.implicitly_wait(60)

	pincode = driver.find_element_by_id('ctl00_Contentplaceholder2_ddlPin')
	pincode.click()
	driver.implicitly_wait(60)
	time.sleep(3)

	slct_optn = driver.find_element_by_xpath('//select[@id="ctl00_Contentplaceholder2_ddlPin"]/option['+str(i+2)+']')
	slct_optn.click()
	driver.implicitly_wait(60)
	time.sleep(3)

	road_names = driver.find_elements_by_xpath('//select[@id="ctl00_Contentplaceholder2_ddlRoadName"]/option')

	for j in range(0,len(road_names)-1)	:

		driver.implicitly_wait(60)

		road_name = driver.find_element_by_id('ctl00_Contentplaceholder2_ddlRoadName')
		act_road_name = ActionChains(driver)
		act_road_name.move_to_element(road_name)
		act_road_name.click(road_name)
		driver.implicitly_wait(60)
		time.sleep(3)

		slct_optn_rd = driver.find_element_by_xpath('//select[@id="ctl00_Contentplaceholder2_ddlRoadName"]/option['+str(j+2)+']')
		slct_optn_rd.click()
		driver.implicitly_wait(60)
		time.sleep(3)

		build_names = driver.find_elements_by_xpath('//select[@id="ctl00_Contentplaceholder2_ddlBuildingName"]/option')

		for k in range(0,len(build_names)-1):

			driver.implicitly_wait(60)

			build_name = driver.find_element_by_id('ctl00_Contentplaceholder2_ddlBuildingName')
			act_build_name = ActionChains(driver)
			act_build_name.move_to_element(build_name)
			act_build_name.click(build_name)
			driver.implicitly_wait(60)
			time.sleep(3)

			slct_optn_build = driver.find_element_by_xpath('//select[@id="ctl00_Contentplaceholder2_ddlBuildingName"]/option['+str(k+2)+']')
			slct_optn_build.click()
			driver.implicitly_wait(60)
			time.sleep(3)

			#write code for storing data


time.sleep(5)
driver.quit()

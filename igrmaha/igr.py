import urllib
from selenium import webdriver
import time
from PIL import Image
import textract
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys

driver = webdriver.Chrome()

year=['2014','2015','2016','2013']
cts = ['3']
for yr in range(0,len(year)):
	for ct in range(0,len(cts)):
		driver.get('https://esearchigr.maharashtra.gov.in/testingesearch/Login.aspx')
		driver.implicitly_wait(40)
		driver.maximize_window()
		driver.implicitly_wait(50)

		userid = driver.find_element_by_id('txtUserid')
		userid.send_keys('ritesh_1')
		driver.implicitly_wait(40)
		time.sleep(5)

		passw = driver.find_element_by_id('txtPswd')
		passw.send_keys('NMPLbhavans123$')
		driver.implicitly_wait(40)
		time.sleep(5)

		image = driver.find_element_by_xpath('//img[@src="Handler.ashx"]')
		location = image.location
		size = image.size
		driver.save_screenshot('/home/karan/scrap_proj/igrmaha/1.png')

		im = Image.open('/home/karan/scrap_proj/igrmaha/1.png')

		left = location['x']
		top = location['y']
		right = location['x'] + size['width']
		bottom = location['y'] + size['height']

		im = im.crop((left,top,right,bottom))
		im.save('/home/karan/scrap_proj/igrmaha/1.png')
		text = textract.process('/home/karan/scrap_proj/igrmaha/1.png')
		text = text.strip()

		capt = driver.find_element_by_id('txtcaptcha')
		capt.send_keys(text)
		driver.implicitly_wait(2)
		time.sleep(2)

		login = driver.find_element_by_id('btnLogin').click()
		driver.implicitly_wait(10)
		time.sleep(5)

		years = driver.find_element_by_xpath('//option[@value="'+year[yr]+'"]').click()
		driver.implicitly_wait(100)
		time.sleep(5)

		sel_city = driver.find_element_by_xpath('//option[@value="31"]').click()
		driver.implicitly_wait(100)
		time.sleep(5)

		vill_name = driver.find_element_by_id('txtAreaName')
		vill_name.send_keys('pava')
		driver.implicitly_wait(100)
		time.sleep(5)

		sel_vill = driver.find_element_by_id('ddlareaname')
		Act_vill = ActionChains(driver)
		Act_vill.move_to_element(sel_vill)
		Act_vill.click(sel_vill).click(sel_vill).perform()
		driver.implicitly_wait(100)
		time.sleep(5)

		sel_village = driver.find_element_by_xpath('//option[@value="Pavai"]').click()
		driver.implicitly_wait(100)
		time.sleep(5)

		prop_no = driver.find_element_by_id('txtAttributeValue')
		prop_no.send_keys(cts[ct])
		driver.implicitly_wait(100)
		time.sleep(5)

		submit = driver.find_element_by_id('Button1').click()
		driver.implicitly_wait(100)
		time.sleep(60)

		sodh = driver.find_element_by_id('btnSearch').click()
		driver.implicitly_wait(100)
		time.sleep(30)

		check = 0
		main_wnw = driver.window_handles[0]

		page_index = driver.find_elements_by_xpath('//table[@id="RegistrationGrid"]/tbody/tr[last()]/td/table/tbody/tr/td')
		print "Page Index is --- {}".format(len(page_index))
		n=2

		while n<=(len(page_index)+1):
			
			driver.implicitly_wait(100)
			index = driver.find_elements_by_xpath('//table[@id="RegistrationGrid"]/tbody/tr')
			print "INDEX II count is --- {}".format(len(index))

			for i in range(2,len(index)):
					
					driver.implicitly_wait(50)
					driver.find_element_by_xpath('//table[@id="RegistrationGrid"]/tbody/tr['+str(i)+']/td/input').click()
					driver.implicitly_wait(300)
					time.sleep(10)
					
					next = driver.window_handles[1]

					driver.switch_to.window(next)
					driver.implicitly_wait(20)

					time.sleep(5)
					f = open('/home/karan/scrap_proj/igrmaha/{}.csv'.format(str('pavai_'+year[yr]+'_'+cts[ct])),'ab')
					keys = driver.find_elements_by_xpath('//body/table[3]/tbody/tr/td[1]')
					if check==0:
						for key in keys:
							text1 = key.text.encode('utf-8')
							print text1
							f.write(text1+'@')
						f.write('\n')
						check=1
					pairs = driver.find_elements_by_xpath('//body/table[3]/tbody/tr/td[2]')
					for pair in pairs:
						text2 = pair.text.encode('utf-8')
						print text2
						f.write(text2+'@')
					f.write('\n')
					f.close()
				
					time.sleep(10)
					driver.close()
					time.sleep(5)

					driver.switch_to.window(main_wnw)
					# print driver.page_source
					
					driver.implicitly_wait(50)
					# time.sleep(10)

			driver.find_element_by_xpath('//table[@id="RegistrationGrid"]/tbody/tr[last()]/td/table/tbody/tr/td['+str(n)+']/a').click()
			if '...' in driver.find_element_by_xpath('//table[@id="RegistrationGrid"]/tbody/tr[last()]/td/table/tbody/tr/td['+str(n)+']').text:
				n=3
			else:
				n=n+1
			driver.implicitly_wait(100)
			time.sleep(20)


		time.sleep(20)
		driver.quit()
		time.sleep(30)

	time.sleep(10)
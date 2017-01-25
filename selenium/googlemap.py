from selenium import webdriver
import os
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
# from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.firefox.webdriver import FirefoxProfile
from datetime import datetime as dt
import time
from pymouse import PyMouse
import pyautogui as m_p

# opdriver = webdriver.ChromeOptions()
# opdriver.add_argument('user-data-dir=/home/karan/.config/google-chrome')
# driver = webdriver.Chrome(executable_path='/usr/bin/chromedriver',chrome_options=opdriver)
driver = webdriver.Chrome()

# time.sleep(5)
driver.get('https://www.google.co.in/maps')
driver.implicitly_wait(300)
driver.maximize_window()
driver.implicitly_wait(300)

time.sleep(20)

search = driver.find_element_by_id('searchboxinput')
search.send_keys('real estate agents')
search.send_keys(Keys.ENTER)
time.sleep(10)

m_p.moveTo(683,384)
m_p.dragRel(0,100,1,button='left')
m_p.moveTo(683,384)
m_p.dragRel(0,100,1,button='left')
m_p.moveTo(683,384)
m_p.dragRel(0,100,1,button='left')
m_p.moveTo(683,384)
m_p.dragRel(0,100,1,button='left')

time.sleep(10)
driver.quit()
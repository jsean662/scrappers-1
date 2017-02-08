from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.common.keys import Keys
# from selenium.webdriver.support.ui import Select
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.common.exceptions import TimeoutException
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.common.exceptions import NoSuchElementException
# from selenium.common.exceptions import NoAlertPresentException
# import sys
import unittest
import time
# import re


class Sel(unittest.TestCase):
    def setUp(self):
        try:
            self.driver = webdriver.Chrome()
            self.driver.implicitly_wait(30)
            self.base_url = "http://www.kolkataproperties.in/search_results.php?buy=yes"
            self.verificationErrors = []
            self.accept_next_alert = True
        except Exception as e:
            print(e)

    def test_sel(self):
        try:
            driver = self.driver
            delay = 3
            driver.get(self.base_url)
            driver.implicitly_wait(40)
            mainclass = driver.find_element_by_class_name("col-md-4 bottom_property")
            driver.implicitly_wait(40)
            print(mainclass)
            for i in range(1, 5):
                self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(2)
            html_source = driver.page_source
            data = html_source.encode('utf-8')
        except Exception as e:
            print(e)


if __name__ == "__main__":
    unittest.main()

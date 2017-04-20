from selenium import webdriver
import time
from selenium.common.exceptions import StaleElementReferenceException, NoSuchElementException, ElementNotSelectableException, ElementNotVisibleException, WebDriverException
import csv
import re


name = mobile_no = address = amount = bill_date = due_date = acc_no = ca_no = email_id = ''
try:
    store_file = open('try.csv', 'w')
    field_names = ['Consumer no', 'Consumer Name', 'Mobile No', 'Email Address', 'Road Name', 'Building Name','Address', 'Pin Code', 'Amount', 'Bill Date', 'Due Date', 'Account No', 'CA No']
    writer = csv.DictWriter(store_file, fieldnames=field_names)
    writer.writeheader()
    driver = webdriver.Chrome()
    driver.get('https://www.bestundertaking.net/QuickPayment.aspx')

    with open('PinCode08.csv', 'r') as f1:
        reader = csv.reader(f1)
        for i in reader:
            try:

                driver.implicitly_wait(60)
                driver.get('https://www.bestundertaking.net/QuickPayment.aspx')
                time.sleep(2)
                input_no = driver.find_element_by_id('ctl00_Contentplaceholder2_ctl02_txtAccno')
                input_no.send_keys('374187004') # '884131013' i[0]
                button = driver.find_element_by_id('ctl00_Contentplaceholder2_ctl02_btnGo')
                button.click()
                driver.implicitly_wait(60)
                time.sleep(2)
                
                try:
                    quick_pay = driver.find_element_by_id('ctl00_Contentplaceholder2_ctl02_btnQuickPay')
                    quick_pay.click()
                    driver.implicitly_wait(60)
                    time.sleep(2)

                    try:

                        make_pay = driver.find_element_by_id('ctl00_Contentplaceholder2_ctl04_btnMakePayment')
                        make_pay.click()
                        driver.implicitly_wait(60)
                        time.sleep(2)

                        acc_no = driver.find_element_by_id('lblACCNO').text.split('-')[0]
                        driver.implicitly_wait(60)

                        ca_no = driver.find_element_by_id('lblACCNO').text.split('-')[1]
                        driver.implicitly_wait(60)

                        name = driver.find_element_by_xpath('.//*[@id="lblNameAddress"]').text
                        # driver.find_element_by_id('lblNameAddress').
                        driver.implicitly_wait(60)

                        if not name == '' or not name == ' ':
                            temp_address = name.split('\n')
                            address = temp_address[1] + temp_address[2]
                            # driver.find_element_by_id('lblNameAddress').text
                            driver.implicitly_wait(60)

                        email_id = driver.find_element_by_id('lblEmail').text
                        driver.implicitly_wait(60)

                        amount = driver.find_element_by_id('lblAmount').text
                        driver.implicitly_wait(60)

                        mobile_no = driver.find_element_by_id('lblMobile').text
                        driver.implicitly_wait(60)

                        bill_date = driver.find_element_by_id('lblBillMonth').text
                        driver.implicitly_wait(60)

                        due_date = 'None'
                    except Exception as e:
                        print(e)

                    # go_back = driver.find_element_by_id('btnBack')
                    # go_back.click()
                    # driver.implicitly_wait(60)
                    # time.sleep(2)

                except Exception as e:
                    print(e)
                    view_pay = driver.find_element_by_id('ctl00_Contentplaceholder2_ctl02_btnViewPayments')
                    view_pay.click()
                    driver.implicitly_wait(60)
                    time.sleep(2)

                    name = i[1]
                    email_id = 'None'

                    address = driver.find_element_by_id('ctl00_Contentplaceholder2_ctl04_LblAddress').text
                    driver.implicitly_wait(60)

                    amount = driver.find_element_by_id('ctl00_Contentplaceholder2_ctl04_lblMsg').text
                    driver.implicitly_wait(60)

                    mobile_no = driver.find_element_by_id('ctl00_Contentplaceholder2_ctl04_lblMobileNumber1').text
                    driver.implicitly_wait(60)

                    bill_date = driver.find_element_by_id('ctl00_Contentplaceholder2_ctl04_lblBillDate').text
                    driver.implicitly_wait(60)

                    due_date = driver.find_element_by_id('ctl00_Contentplaceholder2_ctl04_lblDueDate').text
                    driver.implicitly_wait(60)

                    go_back = driver.find_element_by_id('ctl00_Header1_btnHome')
                    go_back.click()
                    driver.implicitly_wait(60)
                    time.sleep(2)

                # amount = driver.find_element_by_id('ctl00_Contentplaceholder2_ctl04_lblMsg')
                try:
                    amount = re.findall('[0-9]+', amount)[0]
                except Exception as ve:
                    print(ve)
                writer.writerow({'Consumer no': i[0], 'Consumer Name': name, 'Mobile No': mobile_no, 'Email Address': email_id, 'Road Name': i[3], 'Building Name': i[4], 'Address': address, 'Pin Code': i[2], 'Amount': amount, 'Bill Date': bill_date, 'Due Date': due_date, 'Account No': acc_no, 'CA No': ca_no})

            except StaleElementReferenceException as e:
                print(e)
            except ElementNotSelectableException as elx:
                print(elx)
            except ElementNotVisibleException as elvs:
                print(elvs)
            except NoSuchElementException as ns:
                print(ns)
            except Exception as ex:
                print(ex)

    time.sleep(2)
    driver.quit()
except WebDriverException as wx:
    print(wx)
except Exception as ex:
    print(ex)

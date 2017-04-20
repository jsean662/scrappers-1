from selenium import webdriver
import time
import pandas as pd
import csv

driver = webdriver.Chrome()
c = 0

df = pd.read_csv('Own6.csv', encoding='latin1')

fieldnames = ['Name', 'Email Id', 'Date of Birth', 'Mobile No.', 'Current Employer', 'Gender', 'Address', 'Index']

clean = open('Own6_Clean_Sheet.csv', 'a')
unclean = open('Own6_UnClean_Sheet.csv', 'a')

clean_writer = csv.DictWriter(clean, fieldnames=fieldnames)
unclean_writer = csv.DictWriter(unclean, fieldnames=fieldnames)

clean_writer.writeheader()
unclean_writer.writeheader()


df = df.drop_duplicates(subset=['Email Id'])

emails = df['Email Id'].tolist()
'''names = df['name'].tolist()
dob = df['bdate'].tolist()
mobile = df['mobile'].tolist()
curemp = df['com'].tolist()
gend = df['gender'].tolist()
addr = df['address'].tolist()'''

unclean_df = clean_df = pd.DataFrame(columns=df.columns.tolist())

try:

    for i in range(0, len(emails)):
        try:
            if not c == 0:
                driver = webdriver.Chrome()
            if 'gmail' in emails[i]:
                driver.get('https://accounts.google.com/ServiceLogin?service=mail&passive=true&rm=false&continue=https://mail.google.com/mail/?tab%3Dwm&scc=1&ltmpl=default&ltmplcache=2&emr=1&osid=1#identifier')
                time.sleep(3)
                driver.set_page_load_timeout(30)
                driver.implicitly_wait(50)

                email = driver.find_element_by_id('Email')
                email.send_keys(emails[i])
                driver.implicitly_wait(50)
                time.sleep(2)

                next = driver.find_element_by_id('next')
                next.click()
                driver.implicitly_wait(50)
                time.sleep(2)

                # check = '<span id="email-display">' + str(emails[i]) + '</span>'

                if not 'slide-in hide-form' in driver.page_source:
                    clean_df = clean_df.append(df[df['Email Id'] == emails[i]].to_dict('records1'), ignore_index=True)
                    clean_writer.writerow({'Name': df['Name'][i], 'Email Id': emails[i], 'Date of Birth': df['Date of Birth'][i], 'Mobile No.': df['Mobile No.'][i], 'Current Employer': df['Current Employer'][i], 'Gender': df['Gender'][i], 'Address': df['Address'][i], 'Index': i})
                else:
                    unclean_df = unclean_df.append(df[df['Email Id'] == emails[i]].to_dict('records2'), ignore_index=True)
                    unclean_writer.writerow({'Name': df['Name'][i], 'Email Id': emails[i], 'Date of Birth': df['Date of Birth'][i], 'Mobile No.': df['Mobile No.'][i], 'Current Employer': df['Current Employer'][i], 'Gender': df['Gender'][i], 'Address': df['Address'][i], 'Index': i})
            elif 'yahoo' in emails[i] or 'ymail' in emails[i]:
                driver.get('https://login.yahoo.com/config/mail?.intl=my')
                time.sleep(3)
                driver.set_page_load_timeout(30)
                driver.implicitly_wait(50)

                email = driver.find_element_by_id('login-username')
                email.send_keys(emails[i])
                driver.implicitly_wait(50)
                time.sleep(2)

                next = driver.find_element_by_id('login-signin')
                next.click()
                driver.implicitly_wait(50)
                time.sleep(2)

                if not 'passwd-field mbr-hide' in driver.page_source:
                    clean_df = clean_df.append(df[df['Email Id'] == emails[i]].to_dict('records1'), ignore_index=True)
                    clean_writer.writerow({'Name': df['Name'][i], 'Email Id': emails[i], 'Date of Birth': df['Date of Birth'][i], 'Mobile No.': df['Mobile No.'][i], 'Current Employer': df['Current Employer'][i], 'Gender': df['Gender'][i], 'Address': df['Address'][i], 'Index': i})
                else:
                    unclean_df = unclean_df.append(df[df['Email Id'] == emails[i]].to_dict('records2'), ignore_index=True)
                    unclean_writer.writerow({'Name': df['Name'][i], 'Email Id': emails[i], 'Date of Birth': df['Date of Birth'][i], 'Mobile No.': df['Mobile No.'][i], 'Current Employer': df['Current Employer'][i], 'Gender': df['Gender'][i], 'Address': df['Address'][i], 'Index': i})
            elif 'hotmail' in emails[i]:
                driver.get('https://login.live.com/login.srf?wa=wsignin1.0&rpsnv=13&ct=1484911427&rver=6.4.6456.0&wp=MBI_SSL_SHARED&wreply=https:%2F%2Fmail.live.com%2Fdefault.aspx%3Frru%3Dinbox&lc=1033&id=64855&mkt=en-us&cbcxt=mai')
                time.sleep(3)
                driver.set_page_load_timeout(30)
                driver.implicitly_wait(50)

                email = driver.find_element_by_id('i0116')
                email.send_keys(emails[i])
                driver.implicitly_wait(50)
                time.sleep(2)

                next = driver.find_element_by_id('idSIButton9')
                next.click()
                driver.implicitly_wait(50)
                time.sleep(2)

                if 'Enter the password for' in driver.page_source:
                    clean_df = clean_df.append(df[df['Email Id'] == emails[i]].to_dict('records1'), ignore_index=True)
                    clean_writer.writerow({'Name': df['Name'][i], 'Email Id': emails[i], 'Date of Birth': df['Date of Birth'][i], 'Mobile No.': df['Mobile No.'][i], 'Current Employer': df['Current Employer'][i], 'Gender': df['Gender'][i], 'Address': df['Address'][i], 'Index': i})
                else:
                    unclean_df = unclean_df.append(df[df['Email Id'] == emails[i]].to_dict('records2'), ignore_index=True)
                    unclean_writer.writerow({'Name': df['Name'][i], 'Email Id': emails[i], 'Date of Birth': df['Date of Birth'][i], 'Mobile No.': df['Mobile No.'][i], 'Current Employer': df['Current Employer'][i], 'Gender': df['Gender'][i], 'Address': df['Address'][i], 'Index': i})
            else:
                driver.get('https://accounts.google.com/ServiceLogin?service=mail&passive=true&rm=false&continue=https://mail.google.com/mail/?tab%3Dwm&scc=1&ltmpl=default&ltmplcache=2&emr=1&osid=1#identifier')
                time.sleep(3)
                driver.set_page_load_timeout(30)
                driver.implicitly_wait(50)

                email = driver.find_element_by_id('Email')
                email.send_keys(emails[i])
                driver.implicitly_wait(50)
                time.sleep(2)

                next = driver.find_element_by_id('next')
                next.click()
                driver.implicitly_wait(50)
                time.sleep(2)

                if not 'slide-in hide-form' in driver.page_source:
                    clean_df = clean_df.append(df[df['Email Id'] == emails[i]].to_dict('records1'), ignore_index=True)
                    clean_writer.writerow({'Name': df['Name'][i], 'Email Id': emails[i], 'Date of Birth': df['Date of Birth'][i], 'Mobile No.': df['Mobile No.'][i], 'Current Employer': df['Current Employer'][i], 'Gender': df['Gender'][i], 'Address': df['Address'][i], 'Index': i})
                else:
                    unclean_df = unclean_df.append(df[df['Email Id'] == emails[i]].to_dict('records2'), ignore_index=True)
                    unclean_writer.writerow({'Name': df['Name'][i], 'Email Id': emails[i], 'Date of Birth': df['Date of Birth'][i], 'Mobile No.': df['Mobile No.'][i], 'Current Employer': df['Current Employer'][i], 'Gender': df['Gender'][i], 'Address': df['Address'][i], 'Index': i})

            driver.quit()
            time.sleep(1)
            c = 1
        except Exception as e:
            print("Exception in the loop" + str(e))

    clean_df.to_csv('Own6_email_verified.csv')
    unclean_df.to_csv('Own6_email_unverified.csv')
except Exception as e:
    print("Exception out of loop" + str(e))


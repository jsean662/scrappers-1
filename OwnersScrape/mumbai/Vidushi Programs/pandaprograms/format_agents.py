# -*- coding: utf-8 -*-
import pandas as pd
from pandas import DataFrame
import glob
import os
import time
# import fnmatch
# from fuzzywuzzy import fuzz
# from fuzzywuzzy import process
# import jellyfish as jf

# Calculation of Executon time
def hms_string(sec_elapsed):
    h = int(sec_elapsed / (60 * 60))
    m = int((sec_elapsed % (60 * 60)) / 60)
    s = sec_elapsed % 60.
    return "{}:{:>02}:{:>05.2f}".format(h, m, s)

#initializing dataframe
# frm = pd.DataFrame()
# list_ = []

#Reading multiple csv files 
# files = glob.glob('/home/karan/Nexchange/file_aws/new_data_wt_qlty4/mumbai_data/*.csv')
# for fil in files:
# 	df = pd.read_csv(fil,dtype='unicode')
# 	list_.append(df)
# frm = pd.concat(list_)

#reading single csv file
frm = pd.read_csv('C:\Users\OyeOk\Desktop\Scrapy Projects\PANDA programs\\all_CSV_files\oyeok_agents_INPUT.csv')

#reading each file including folders and converting to one csv file and loading into dataframe
# for dirpath, dirs, files in os.walk('/home/karan/Nexchange/file_aws/new_data_wt_qlty4'):
#     for filename in fnmatch.filter(files, '*.csv'):
#         print(os.path.join(dirpath, filename))
#         df = pd.read_csv(os.path.join(dirpath, filename),dtype='unicode')
#         list_.append(df)
# frm = pd.concat(list_)

#Removing Duplicates from dataframe based on selected columns
dup = frm.drop_duplicates(subset=['company_name', 'contact_person', 'phone_no', 'mobile_no', 'email_id', 'city', 'locality', 'sublocality', 'pincode', 'address', 'platform', 'data_id', 'add_lat', 'add_longt'],keep='last').reset_index()
del dup['index']

# freezing column output
arrng_column = ['data_id', 'platform', 'company_name', 'contact_person', 'phone_no', 'mobile_no', 'email_id', 'city', 'locality', 'sublocality', 'pincode', 'address', 'add_lat', 'add_longt', 'scraped_time']

arrng_dup =  dup[arrng_column]

# To change column values or replace with own string
# df.loc[:,'<column name>'] = df['<column name>'].replace(to_replace=[<add str to change>,<add str to change>,..],value=<value>,inplace=True)
#     OR
# df.replace(to_replace={'<column name>':{'str to change':'to this value','':'',...}})
# arrng_dup.loc[:,'Building_name'] = arrng_dup['Building_name'].replace(to_replace=[' ','None',', Bandra (west), Mumbai South West',', No Part','1 Rk Now As Chsl',',..','.','10 Min From Bamabdongri Rly Stn, Sec-20,ulwe','10 Min From Bamabdongri Rly.stn.sec-16 ,ulwe','10 Min From Bamabdongri Rly.stn.sec-19,ulwe','10 Min From Bamabdongri Rly.stn.sec-19,ulwe,','10 Min From Bamabdongri Rly.stn.sec-23,ulwe','10 Min From Bamandongri Rly.stn.sec-08,ulwe','10 Min From Bamandongri Rly.stn.sec-10-b,ulwe','10 Min From Bamandongri Rly.stn.sec-17 ,ulwe','10 Min From Bamandongri Rly.stn.sec-17,ulwe','10 Min From Bamandongri Rly.stn.sec-18,ulwe','10 Mins From Nerul Rly.stn.sec-28.nerul','10 Mins From Seawoods Rly.stn.sec-50e,seawoods','10 Mins From Targhar Rly Stn, Sec-2, Ulwe','10 Mints From Sanpada Rly.stn.sec-04,','10 Mints From Sanpada Rly.stn.sec-04, Sanpada','10 Mints From Sanpada.rly.stn.sec-15','10mins From Bamandogri Rly.stn.sec-21, Ulwe','10mins Walk From Bamandongri Rly.stn.sec-08,ulwe','10mins Walk From Bamandongri Rly.stn.sec-21,ulwe','10mints From Belapur Rly.stn.sec-30/31 Belapur','10mints From Seawoods Rly Stn.sec-50','10mints From Seawoods Rly Stn.sec-50,','10mints From Seawoods Rly Stn.sec-50,seawoods','11th Road Chembur','128355','12th Road','1349','134931','13th Rd','14 Number Road, Chembur','14 Th Rd','14th Road','14th road','15 Th Rd','15874','15TH ROAD','15min From Bamandongri Rly. Stn,sec-9,ulwe','15th Road','15th Road Khar West','16164','16th Rd','16th Rd Khar','16th Road','17th Road','18th Road','18th Road Khar','1bhk','1bhk Aprtment','1bhk Spacious Flat','1bhk rent','2 Bed Apartment','2 Bed Apartment Khar West','2 Bed Sea View Apartment','2 Bed Spacious','2 Bed Spacious Apartmemnt','2 Bed Spacious Apartment','2 Bed Spacious Sea View Apartment','2 Bhk Near Kharkopar Station','2,4,8,7,floor','20 80 scheme for few bookings only','21st Road','25 South','29764','2bhk Apartments 970 To 1000sqft A Grade Developer','2bhk Flat On Request','2mins Walking From Bamandongri Rly.stn.sec-19','2nd Floor','3 BHk on lease in very posh location at powai','3 Bhk Luxurious Apartment','3 Bhk Premium Apartment','3 bhk flat sec 6','3 bhk rent','30th Road','32 Meter Row House','36 Acres Of Prelaunch Project','360 West','39 No. Society Malvani Malad West','3bhk regency gardens kharghar','3bhk villa Sector 28','4 Bhk Luxurious Apartment','4 Bungalow','4 Bunglows , Andheri West','4 bhk bunglow','5min Walking From Cbd Belapur Rly.stn.sec-30/31', '5mins From Kharkhopar Rly.stn.sec-16', '5mins From Kharkhopar Rly.stn.sec-17', '5mins From Kharkhopar Rly.stn.sec-17,ulwe', '5mins From Kharkopar Rly.stn.sec-16', '5mins From Kharkopar Rly.stn.sec-17', '5mins From Nerul Rly.stn.sec-28.nerul', '5mins From Palmbeach Rd.sec-18,palm Beach', '5mins From Seawoods Rly.stn.sec-46/a', '5mins From Seawoods Rly.stn.sec-50', '5mins From Seawoods Rly.stn.sec-54/56/58,seawoods', '5mins From Targhar Rly.stn.sec-03', '5mins From Vashi Rly.stn.sec-30a', '5mins Walking From Bamandongri Rly.stn.sec-19', '5mins Walking From Bamandongri Rly.stn.sec-19,', '5mins Walking From Bamandongri Rly.stn.sec-19, Ulw', '5mints From Bamandongari Rly.stn.sec-05', '5mints From Bamandongari Rly.stn.sec-05,ulwe', '5mints From Bamandongari Rly.stn.sec-08,ulwe', '5mints From Bamandongari Rly.stn.sec-08,ulwe,', '5mints From Bamandongari Rly.stn.sec-09,ulwe', '5mints From Bamandongari Rly.stn.sec-10b,ulwe', '5mints From Bamandongari Rly.stn.sec-16,ulwe', '5mints From Bamandongari Rly.stn.sec-16,ulwe,', '5mints From Bamandongari Rly.stn.sec-17', '5mints From Bamandongari Rly.stn.sec-17, Ulwe', '5mints From Bamandongari Rly.stn.sec-17,ulwe', '5mints From Bamandongari Rly.stn.sec-17,ulwe,', '5mints From Bamandongari Rly.stn.sec-17,ulwe,,', '5mints From Bamandongari Rly.stn.sec-18,ulwe', '5mints From Bamandongari Rly.stn.sec-18,ulwe,', '5mints From Bamandongari Rly.stn.sec-19', '5mints From Bamandongari Rly.stn.sec-19, Ulwe', '5mints From Bamandongari Rly.stn.sec-19,ulwe', '5mints From Bamandongari Rly.stn.sec-19b', '5mints From Bamandongari Rly.stn.sec-19ulwe', '5mints From Bamandongari Rly.stn.sec-20', '5mints From Bamandongari Rly.stn.sec-20, Ulwe', '5mints From Bamandongari Rly.stn.sec-20, Ulwe,', '5mints From Bamandongari Rly.stn.sec-20,ulwe', '5mints From Bamandongari Rly.stn.sec-21 ,ulwe', '5mints From Bamandongari Rly.stn.sec-21,ulwe', '5mints From Bamandongari Rly.stn.sec-21,ulwe,', '5mints From Bamandongari Rly.stn.sec-23', '5mints From Bamandongari Rly.stn.sec-23,ulwe', '5mints From Bamandongari Rly.stn.sec-23,ulwe,', '5mints From Kharkopar Rly.stn.sec-16/a', '5mints From Kharkopar Rly.stn.sec-17', '5mints From Kharkopar Rly.stn.sec-18,ulwe', '5mints From Kharkopar Rly.stn.sec-18,ulwe,', '5mints From Sanpada Rly.stn.sec-15,sanpada', '5mints From Sanpada Rly.stn.sec-19,sanpada', '5mints From Seawoods Rly.stn.sec-38', '5mints From Seawoods Rly.stn.sec-46/a', '5mints From Seawoods Rly.stn.sec-50,seawoods', '5mints From Seawoods.rly.stn.sec-46/a,seawoods', '5mints From Seawoods.rly.stn.sec-50', '5mints From Seawoods.rly.stn.sec-50, Seawoods', '5mints From Seawoods.rly.stn.sec-50,seawoods', '5mints From Targhar Rly.stn.sec-03,ulwe', '5mints From Targhar Rly.stn.sec-03,ulwe,', '5mints Walking From Nerul Rly.stn.sec-21', '5mints Walking From Nerul Rly.stn.sec-27,nerul', '5mints Walking From Nerul Rly.stn.sec-27,nerul,', '5mints Walking From Nerul Rly.stn.sec-28', '5mints Walking From Nerul Rly.stn.sec-28,', '5mints Walking From Nerul Rly.stn.sec-28, Nerul', '5mints Walking From Nerul Rly.stn.sec-28,nerul', '5mints Walking From Nerul Rly.stn.sec-28,nerul,', '5mints Walking From Nerul Rly.stn.sec-29,nerul,', '5mints Walking From Seawoods Rly.stn.sec-36', '5mints Walking From Seawoods Rly.stn.sec-38', '5mints Walking From Seawoods Rly.stn.sec-38.', '5mints Walking From Seawoods Rly.stn.sec-38.,', '5mints Walking From Seawoods Rly.stn.sec-46/a', '40 Mtr Row House " Pratik"','45776','4bunglow', '4bunglows','5 Mins From Kharghar Rly.stn.sec-08,kharghar', '5 Mins From Nerul Rly Stn, Sec-27, Nerul', '5 Mins From Nerul Rly Stn, Sec-28,nerul', '5 Mins From Nerul Rly.stn.sec-28.nerul', '5 Mins From Nerul Rly.stn.sec-29.nerul', '52124','5th Floor', '60ft','6th Floor', '6th Flr', '7', '7 Bungalow','7 Bunglows','7bunglow','7bunglows', '7th Floor', '7th Road Khar West','7thfloor','827', '8t Floor', '8th Floor','9th Floor','Aabbccdd', 'Aabee','Agksptptoskofgpy','Apartment', 'Apartment In Mumbai Thane, Mumbai', 'Apartment In Thane West, Thane', 'Apartment, Bandra (west), Mumbai South West', 'Apartment, Seven Bungalow, Andheri West','As Per Request','At Kavesar, Thane West','Available 4bhk awesomely furnished at a location behind Olps church','Azad Lane', 'Azad Nagar', 'Azad Nagar Behind Apna Bazaar','Azad Road', 'Azadegaon Dombivli East','Band Stand','Bandra','Bandra Bandstand','Bandra Kurla Complex', 'Bandra Kurla Complex \xe2\x80\x93 BKC', 'Bandra Reclamation','Bandra West','Bandra reclemation','Bandra west near otis club','Bandstand',],value='oyeok')

arrng_dup.loc[:,'phone_no'] = arrng_dup['phone_no'].replace(to_replace=[' ','---','null',],value='None')
# To remove row which unwanted str from perticular column(this will remove entire row)
# df[df['<column name>'].isin(['str to remove','str to remove',....])==False] 
# rmv_unwntd_str_row = arrng_dup[arrng_dup['Building_name'].isin(['Karan'])==False]

# sorting data 
sort_fil = arrng_dup.sort_values(['mobile_no','phone_no','email_id','company_name','contact_person','locality','platform'])
# sort_rmv_str_row = rmv_unwntd_str_row.sort_values(['Building_name','lat','longt','Bua_sqft','carpet_area','config_type','Selling_price','Monthly_Rent','price_per_sqft','quality4'])

#Assingning default values as None
final_fil = sort_fil.fillna('None')


# print sort_fil
final_fil.to_csv('C:\Users\OyeOk\Desktop\Scrapy Projects\PANDA programs\OUTPUT_CSV_files\oyeok_agents_OUTPUT.csv', index=False)

#grp_sorted_data = sort_fil.groupby(['email_id', 'phone_no'], as_index=False).sum()

#grp_sorted_data.to_csv('C:\Users\OyeOk\Desktop\Scrapy Projects\PANDA programs\\all_CSV_files\oyeok_agents_OUTPUT.csv', index=False)

# print grp_sorted_data.groups

# email = grp_sorted_data.groups.keys()
# cluster = []

# for name1 in build_name:
# 	for name2 in build_name:
		
# build_name = sort_fil['Building_name'].tolist()
# print len(build_name)

# uniq_build_name = sort_fil['Building_name'].unique().tolist()
# print uniq_build_name
# print len(uniq_build_name)










#setting index as building_name followed by lat and long
# frm.reset_index().set_index(['Building_name','lat','longt']).sortlevel(0).to_csv('/home/karan/Nexchange/file_aws/test_out_csv_pandas/test.csv')
# ordered_frm = frm.reset_index().set_index(['Building_name','lat','longt']).sortlevel(0)
# del ordered_frm['index']
# print frm.columns

# dup.to_csv('/home/karan/Nexchange/file_aws/test_out_csv_pandas/merge_dup.csv')
# print frm
# ttl = spark['Building_name'].count()
# unq = spark['Building_name'].unique()
# print spark.groupby(['Building_name','lat','longt']).count()
# print ttl,len(unq)
# spark.reset_index().set_index(['Building_name','lat','longt']).sortlevel(0).to_csv('/home/karan/Nexchange/files from aws/test_out_csv_pandas/test.csv')

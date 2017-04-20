# -*- coding: utf-8 -*-
import pandas as pd
from pandas import DataFrame
import glob
import os
import fnmatch
import time

#initializing dataframe
frm = pd.DataFrame()
list_ = []

#reading single csv file
# spark = pd.read_csv('C:/Users/OyeOk/Desktop/Scrapy Projects/PANDA programs/all_CSV_files/buildings/banglore/acresrentBangalore/2017-01-26T06-07-44.csv')

# print(spark)

# Reading multiple csv files 
# files = glob.glob('/home/karan/Nexchange/client_oyeok_used/*.csv')

# reading each file and converting to one csv file and loading into dataframe
# for fil in files:
# 	df = pd.read_csv(fil,dtype='unicode')
# 	list_.append(df)
# frm = pd.concat(list_)

#reading each file including folders and converting to one csv file and loading into dataframe
for dirpath, dirs, files in os.walk('C:/Users/OyeOk/Desktop/Scrapy Projects/PANDA programs/test_data_in'):
    for filename in fnmatch.filter(files, '*.csv'):
        print(os.path.join(dirpath, filename))
        df = pd.read_csv(os.path.join(dirpath, filename),dtype='unicode')
        list_.append(df)
frm = pd.concat(list_)

rst_frm = frm.reset_index()

del rst_frm['index']
rst_frm.to_csv('C:/Users/OyeOk/Desktop/Scrapy Projects/PANDA programs/test_data_out/_TEST.csv', index=False)


# print (list(rst_frm))
# print len(list(rst_frm))
# -*- coding: utf-8 -*-
import pandas as pd
from pandas import DataFrame
import glob
import os


#Reading multiple csv files 
files = glob.glob('D:/Python Projects/Scraping/selenium/reference/pandaprograms/Only_Vidushi_Records/*.csv')

#initializing dataframe
frm = pd.DataFrame()
list_ = []

#reading each file and converting to one csv file and loading into dataframe
for fil in files:
	df = pd.read_csv(fil,dtype='unicode')
	list_.append(df)
frm = pd.concat(list_)

rst_frm = frm.reset_index()
del rst_frm['index']

# print(rst_frm)

rst_frm.to_csv('D:/Python Projects/Scraping/selenium/reference/pandaprograms/Only_Vidushi_Records/OUTPUT.csv', index=False)
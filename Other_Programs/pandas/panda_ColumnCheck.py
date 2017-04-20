# -*- coding: utf-8 -*-
import pandas as pd
from pandas import DataFrame
import glob
import os
import fnmatch

# initializing dataframe
frm = pd.DataFrame()
list = []


# print(spark)

# Reading multiple csv files
file_list = []
working_dir = "./residential/pune/"

for root, dirs, files in os.walk(working_dir):
    for filename in files:
        file_list.append(root + "/" + filename)

df_list = [pd.read_csv(file) for file in file_list]
final_df = pd.concat(df_list)
cities = final_df['city'].tolist()
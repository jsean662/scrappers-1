import time
from datetime import datetime
import pandas as pd
import os


final_df = pd.DataFrame()

file_list = []
working_dir = "./residential/pune/"

for root, dirs, files in os.walk(working_dir):
    for filename in files:
        file_list.append(root + "/" + filename)

df_list = [pd.read_csv(file) for file in file_list]
final_df = final_df.append(pd.concat(df_list))
listing_dates = final_df['listing_date'].tolist()
updated_dates = final_df['updated_date'].tolist()
scraped_times = final_df['scraped_time'].tolist()

# dt = '02/09/2017'
# # final_df['listing_date'][0]
# print("First Date : ", dt)
# if ':' in dt:
#     conv_date = time.mktime(datetime.strptime(dt, "%d/%m/%Y HH:MM:SS").timetuple())
# else:
#     conv_date = time.mktime(datetime.strptime(dt, "%d/%m/%Y").timetuple())
# print("Converted Unix Date : ", conv_date)
# date1 = datetime.fromtimestamp(conv_date).strftime('%Y-%m-%d %H:%M:%S')
# print("Last Conversion : ", date1)

for i in range(len(listing_dates)):
    print(final_df['listing_date'][i])
    if ':' in final_df['listing_date'][i]:
        time.mktime(datetime.strptime(final_df['listing_date'][i], "%d/%m/%Y HH:MM:SS").timetuple())
    else:
        time.mktime(datetime.strptime(final_df['listing_date'][i], "%d/%m/%Y").timetuple())

for i in range(len(updated_dates)):
    print(final_df['listing_date'][i])
    if ':' in final_df['updated_date'][i]:
        time.mktime(datetime.strptime(final_df['updated_date'][i], "%d/%m/%Y HH:MM:SS").timetuple())
    else:
        time.mktime(datetime.strptime(final_df['updated_date'][i], "%d/%m/%Y").timetuple())

for i in range(len(scraped_times)):
    print(final_df['listing_date'][i])
    if ':' in final_df['listing_date'][i]:
        time.mktime(datetime.strptime(final_df['scraped_time'][i], "%d/%m/%Y HH:MM:SS").timetuple())
    else:
        time.mktime(datetime.strptime(final_df['scraped_time'][i], "%d/%m/%Y").timetuple())

final_df.to_csv('./final.csv')
import json

from pprint import pprint


def execute_query(df):
    print(df)


JSON_DATA = open('world_bank.json', 'rU', encoding='utf-8')
pprint(json.loads(JSON_DATA.read()))

# with open('world_bank.json', 'r') as data_file:
#     data = json.loads(data_file)

# pprint(data)

SAMPLE_DATA = {
    0: {'First_Name': 'Vikramsingh', 'Last Name': 'Nimbalkar', 'Address': 'Mumbai',  'No': '1234567890', 'College': 'S.P.I.T' },
    1: {'First_Name': 'Vikramsingh', 'Last Name': 'Nimbalkar', 'Address': 'Mumbai',  'No': '1234567890', 'College': 'S.P.I.T' },
    2: {'First_Name': 'Vikramsingh', 'Last Name': 'Nimbalkar', 'Address': 'Mumbai',  'No': '1234567890', 'College': 'S.P.I.T' },
    3: {'First_Name': 'Vikramsingh', 'Last Name': 'Nimbalkar', 'Address': 'Mumbai',  'No': '1234567890', 'College': 'S.P.I.T' },
    4: {'First_Name': 'Vikramsingh', 'Last Name': 'Nimbalkar', 'Address': 'Mumbai',  'No': '1234567890', 'College': 'S.P.I.T' },
}

# print(SAMPLE_DATA.keys())
# for i in range(len(SAMPLE_DATA)):
    # print(SAMPLE_DATA[i]['First_Name'])
    # str = "INSERT INTO TABLE_NAME VALUES('" + SAMPLE_DATA[i]['First_Name'] + "','" + SAMPLE_DATA[i][
    #     'Last Name'] + "','" + SAMPLE_DATA[i]['Address'] + "'," + SAMPLE_DATA[i]['No'] + ",'" + SAMPLE_DATA[i][
    #           'College'] + "')"
    # execute_query(str)


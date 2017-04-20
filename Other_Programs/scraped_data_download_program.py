import os
import pandas as pd
import boto3

os.system('')
# download = boto3.client('s3')
# def get_directory(directory_path, download_path, exclude_file_names):
#     # prepare session
#     session = Session(aws_access_key_id, aws_secret_access_key, region_name)
#
#     # get instances for resource and bucket
#     resource = session.resource('s3')
#     bucket = resource.Bucket(bucket_name)
#
#     for s3_key in self.client.list_objects(Bucket=self.bucket_name, Prefix=directory_path)['Contents']:
#         s3_object = s3_key['Key']
#         if s3_object not in exclude_file_names:
#             bucket.download_file(file_path, download_path + str(s3_object.split('/')[-1])

s3 = boto3.client('s3')
list = s3.list_objects(Bucket='oyeok-scrape')['Contents']
for s3_key in list:
    s3_object = s3_key['residential']
    if not s3_object.endswith("/"):
        s3.download_file('oyeok-scrape', s3_object, s3_object)
    else:
        if not os.path.exists(s3_object):
            os.makedirs(s3_object)

# os.system('cd residential')
final_df = pd.DataFrame()
citynames = os.listdir('./residential')

for cityname in citynames:
    file_list = []
    working_dir = "./residential/" + cityname + "/"

    for root, dirs, files in os.walk(working_dir):
        for filename in files:
            file_list.append(root + "/" + filename)

    df_list = [pd.read_csv(file) for file in file_list]
    final_df = final_df.append(pd.concat(df_list))

    # Default city name would be cityname variable value
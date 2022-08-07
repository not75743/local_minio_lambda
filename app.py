import json
import urllib.parse
import boto3
import gzip
import shutil
import os
print('Loading function')

s3 = boto3.client('s3', endpoint_url='http://minio:9000', aws_access_key_id='minio', aws_secret_access_key='minio123')

def lambda_handler(event, context):

    frombucket = event['Records'][0]['s3']['bucket']['name']
    tobucket = 'cat'
    key = urllib.parse.unquote_plus(event['Records'][0]['s3']['object']['key'], encoding='utf-8')
    zipkey = '{}.gz'.format(key)
    key_array = key.split('/')
    key_filename = key_array[-1]
    filepass = '/tmp/{}'.format(key_filename)
    zipfilepass = '{}.gz'.format(filepass)
    
    try:
        # https://boto3.amazonaws.com/v1/documentation/api/latest/guide/s3-example-download-file.html
        
        s3.download_file(frombucket, key, filepass)
        
        # ファイルzip転送
        with open(filepass, 'rb') as f_in:
            with gzip.open(zipfilepass, 'wb') as f_out:
                shutil.copyfileobj(f_in, f_out)
        files = os.listdir('/tmp')
        s3.upload_file(zipfilepass, tobucket, zipkey)
        
    except Exception as e:
        print(e)
        print('Error getting object {} from bucket {}. Make sure they exist and your bucket is in the same region as this function.'.format(key, bucket))
        raise e

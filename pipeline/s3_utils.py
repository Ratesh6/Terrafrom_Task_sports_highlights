import boto3
import os

AWS_REGION = os.getenv("AWS_REGION")

def upload_file(local_file, bucket, s3_key):
    s3 = boto3.client("s3", region_name=AWS_REGION)
    s3.upload_file(local_file, bucket, s3_key)

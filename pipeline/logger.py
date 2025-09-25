# logger.py
import logging
import boto3
import os

def setup_logger(log_file="pipeline.log"):
    logger = logging.getLogger("sports_pipeline")
    logger.setLevel(logging.INFO)

    # Console handler
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    ch.setFormatter(formatter)
    logger.addHandler(ch)

    # File handler
    fh = logging.FileHandler(log_file)
    fh.setLevel(logging.INFO)
    fh.setFormatter(formatter)
    logger.addHandler(fh)

    return logger

def upload_log_to_s3(log_file="pipeline.log"):
    s3_bucket = os.getenv("S3_BUCKET_LOGS")
    if not s3_bucket:
        raise Exception("S3_BUCKET_LOGS not set in .env")

    if not os.path.exists(log_file):
        print(f"Log file {log_file} does not exist. Skipping upload.")
        return

    s3_client = boto3.client("s3", region_name=os.getenv("AWS_REGION"))
    s3_key = f"logs/{log_file}"
    s3_client.upload_file(log_file, s3_bucket, s3_key)
    print(f"Uploaded {log_file} to s3://{s3_bucket}/{s3_key}")

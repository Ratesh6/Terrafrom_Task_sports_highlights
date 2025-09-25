import boto3
import os

AWS_REGION = os.getenv("AWS_REGION")
S3_BUCKET_VIDEOS = os.getenv("S3_BUCKET_VIDEOS")

def submit_mediaconvert_job(input_s3_key, league, date_str):
    mc = boto3.client("mediaconvert", region_name=AWS_REGION, endpoint_url=get_mediaconvert_endpoint())
    
    output_path = f"s3://{S3_BUCKET_VIDEOS}/processed/{league}/{date_str}/"
    
    job_settings = {
        "Settings": {
            "OutputGroups": [{
                "Name": "File Group",
                "OutputGroupSettings": {
                    "Type": "FILE_GROUP_SETTINGS",
                    "FileGroupSettings": {"Destination": output_path}
                },
                "Outputs": [
                    {"ContainerSettings": {"Container": "MP4"},
                     "VideoDescription": {"CodecSettings": {"Codec": "H_264", "H264Settings": {"MaxBitrate": 5000000}}, "Width": 1280, "Height": 720}},
                    {"ContainerSettings": {"Container": "MP4"},
                     "VideoDescription": {"CodecSettings": {"Codec": "H_264", "H264Settings": {"MaxBitrate": 2500000}}, "Width": 854, "Height": 480}}
                ]
            }],
            "Inputs": [{"FileInput": f"s3://{S3_BUCKET_VIDEOS}/{input_s3_key}"}]
        }
    }
    
    response = mc.create_job(**job_settings)
    return response["Job"]["Id"]

def get_mediaconvert_endpoint():
    mc_client = boto3.client("mediaconvert", region_name=AWS_REGION)
    endpoints = mc_client.describe_endpoints()
    return endpoints["Endpoints"][0]["Url"]

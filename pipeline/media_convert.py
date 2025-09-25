import os
import boto3

def submit_mediaconvert_job(s3_key, league, date_str):
    mediaconvert_client = boto3.client(
        'mediaconvert',
        region_name=os.getenv("AWS_REGION")
    )

    # Example MediaConvert job settings
    job_settings = {
        "Role": os.getenv("MEDIACONVERT_ROLE_ARN"),
        "Settings": {
            "OutputGroups": [
                {
                    "Name": "File Group",
                    "OutputGroupSettings": {
                        "Type": "FILE_GROUP_SETTINGS",
                        "FileGroupSettings": {
                            "Destination": f"s3://{os.getenv('S3_BUCKET_VIDEOS')}/processed/{league}/{date_str}/"
                        }
                    },
                    "Outputs": [
                        {
                            "Preset": "System-Ott_720p",
                            "NameModifier": "_720p"
                        },
                        {
                            "Preset": "System-Ott_480p",
                            "NameModifier": "_480p"
                        }
                    ]
                }
            ],
            "Inputs": [
                {
                    "FileInput": f"s3://{os.getenv('S3_BUCKET_VIDEOS')}/{s3_key}"
                }
            ]
        }
    }

    response = mediaconvert_client.create_job(**job_settings)
    return response['Job']['Id']

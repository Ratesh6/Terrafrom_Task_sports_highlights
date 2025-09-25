import random
import requests
import os
import logging
from s3_utils import upload_file

# Setup logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

# Environment variables
S3_BUCKET_VIDEOS = os.getenv("S3_BUCKET_VIDEOS")
LEAGUE = os.getenv("LEAGUE", "NCAA")
DATE = os.getenv("DATE")  # Optional, defaults to current date in main pipeline if not set

def download_random_video(highlights_data, date_str):
    """
    Downloads a random video from highlights_data and uploads it to S3.
    
    Args:
        highlights_data (dict): JSON data containing highlights.
        date_str (str): Date string for folder structure (YYYY-MM-DD).
    
    Returns:
        tuple: (local filename, S3 key)
    """
    if not highlights_data.get("highlights"):
        logging.error("No highlights found in the data.")
        raise ValueError("No highlights found")

    video_info = random.choice(highlights_data["highlights"])
    video_url = video_info.get("video_url")
    video_id = video_info.get("id")
    
    if not video_url or not video_id:
        logging.error("Invalid video data: missing 'video_url' or 'id'.")
        raise ValueError("Invalid video data")
    
    local_file = f"{video_id}.mp4"
    
    logging.info(f"Downloading video {video_id} from {video_url}...")
    try:
        response = requests.get(video_url, timeout=60)
        response.raise_for_status()
        with open(local_file, "wb") as f:
            f.write(response.content)
    except requests.RequestException as e:
        logging.error(f"Failed to download video: {e}")
        raise

    s3_key = f"incoming/{LEAGUE}/{date_str}/{local_file}"
    
    logging.info(f"Uploading video to S3 bucket '{S3_BUCKET_VIDEOS}' with key '{s3_key}'...")
    upload_file(local_file, S3_BUCKET_VIDEOS, s3_key)
    
    logging.info(f"Video {video_id} successfully uploaded to S3.")
    return local_file, s3_key

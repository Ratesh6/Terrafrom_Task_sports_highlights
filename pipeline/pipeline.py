import os
from datetime import datetime
from dotenv import load_dotenv
from logger import setup_logger, upload_log_to_s3
from fetch_highlights import fetch_highlights
from download_video import download_random_video
from media_convert import submit_mediaconvert_job

# Load environment variables
load_dotenv()

# Setup logger with timestamped log file
log_filename = f"pipeline_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}.log"
logger = setup_logger(log_file=log_filename)

def main():
    date_str = datetime.utcnow().strftime("%Y-%m-%d")
    logger.info(f"Pipeline started for {date_str}")

    try:
        # Fetch highlights from RapidAPI
        highlights_data = fetch_highlights(date_str)
        if not highlights_data:
            logger.warning("No highlights available. Exiting pipeline.")
            return

        logger.info("Highlights JSON fetched successfully.")

        # Download a random video from highlights
        video_file, s3_video_key = download_random_video(highlights_data, date_str)
        logger.info(f"Video downloaded and uploaded to S3: {video_file} -> {s3_video_key}")

        # Submit AWS MediaConvert job for transcoding
        job_id = submit_mediaconvert_job(s3_video_key, os.getenv("LEAGUE"), date_str)
        logger.info(f"MediaConvert job submitted: Job ID = {job_id}")

        logger.info("Pipeline completed successfully.")

    except Exception as e:
        logger.exception(f"Pipeline failed: {e}")

    finally:
        # Upload local log file to S3 logs bucket
        try:
            upload_log_to_s3(log_filename)
            logger.info(f"Pipeline log uploaded to S3: {log_filename}")
        except Exception as e:
            logger.error(f"Failed to upload log to S3: {e}")

if __name__ == "__main__":
    main()
import os
import json
import requests
from dotenv import load_dotenv
from logger import setup_logger

# Load environment variables
load_dotenv()

RAPIDAPI_KEY = os.getenv("RAPIDAPI_KEY")
RAPIDAPI_HOST = os.getenv("RAPIDAPI_HOST")
LEAGUE = os.getenv("LEAGUE")

if not RAPIDAPI_KEY or not RAPIDAPI_HOST:
    raise EnvironmentError(
        "Missing RapidAPI credentials! Set RAPIDAPI_KEY and RAPIDAPI_HOST in your .env file."
    )

logger = setup_logger("fetch_highlights.log")
logger.info(f"RapidAPI Key loaded: {RAPIDAPI_KEY}")
logger.info(f"RapidAPI Host loaded: {RAPIDAPI_HOST}")

BASE_URL = f"https://{RAPIDAPI_HOST}/highlights-by-league"  # Correct endpoint

def fetch_highlights(date_str):
    headers = {
        "X-RapidAPI-Key": RAPIDAPI_KEY,
        "X-RapidAPI-Host": RAPIDAPI_HOST
    }
    params = {"league": LEAGUE, "date": date_str}

    try:
        logger.info(f"Fetching highlights for {LEAGUE} on {date_str}...")
        response = requests.get(BASE_URL, headers=headers, params=params)

        # Handle specific HTTP errors
        if response.status_code == 401:
            logger.error("Unauthorized (401). Check your RapidAPI key and subscription plan.")
            return []
        if response.status_code == 403:
            logger.error("Forbidden (403). Make sure your key is subscribed to this endpoint.")
            return []
        if response.status_code == 404:
            logger.warning(f"No highlights found for {LEAGUE} on {date_str}.")
            return []

        response.raise_for_status()
        data = response.json()

        # Save locally
        json_filename = f"highlights_{date_str}.json"
        with open(json_filename, "w") as f:
            json.dump(data, f, indent=2)
        logger.info(f"Highlights data saved locally: {json_filename}")

        return data

    except requests.exceptions.RequestException as e:
        logger.error(f"HTTP error while fetching highlights: {e}")
        return []

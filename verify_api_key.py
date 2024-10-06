import argparse
import requests
import re
import logging
import time
from datetime import datetime, timedelta

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler()]
)

def verify_api_key(api_key):
    # Validate API key format
    if not bool(re.match(r'^sk-[a-zA-Z0-9\-_]+$', api_key)):
        logging.error("API key format is invalid.")
        return False

    # Create a session to reuse the connection
    with requests.Session() as session:
        session.headers.update({
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        })

        # Verify the API key by making a simple completion request
        if not validate_api_key(session):
            return False

        # Optionally, include information about available models
        list_models(session)

        # Optionally, include account usage details
        get_account_usage(session)

    return True

def validate_api_key(session):
    """Function to validate the provided API key by making a sample request."""
    api_url = "https://api.openai.com/v1/chat/completions"
    payload = {
        "model": "gpt-4",
        "messages": [
            {"role": "user", "content": "This is a test message to validate the API key."}
        ],
        "max_tokens": 1
    }

    try:
        response = session.post(api_url, json=payload)
        response.raise_for_status()

        # Log additional information about the API key from headers
        rate_limit = response.headers.get('x-ratelimit-limit-requests', 'Unknown')
        rate_remaining = response.headers.get('x-ratelimit-remaining-requests', 'Unknown')
        reset_time = response.headers.get('x-ratelimit-reset-requests', 'Unknown')

        logging.info("API key validation successful.")
        logging.info(f"Rate Limit: {rate_limit}")
        logging.info(f"Rate Limit Remaining: {rate_remaining}")
        logging.info(f"Rate Limit Reset Time (Raw): {reset_time}")

        # Parse reset time and calculate future reset time
        if reset_time != 'Unknown':
            try:
                reset_time_seconds = float(re.sub(r'[^\d.]', '', reset_time))  # Remove non-numeric characters except '.'
                reset_time_future = datetime.now() + timedelta(seconds=reset_time_seconds)
                reset_time_human = reset_time_future.strftime('%Y-%m-%d %H:%M:%S')
                logging.info(f"Rate Limit Reset Time (Local): {reset_time_human}")
            except ValueError:
                logging.error(f"Could not parse rate limit reset time: {reset_time}")

        return True
    except requests.exceptions.RequestException as e:
        logging.error(f"Error during API key validation: {e}")
        return False

def list_models(session):
    """Optional function to list available models for the provided API key."""
    api_url = "https://api.openai.com/v1/models"

    try:
        response = session.get(api_url)
        response.raise_for_status()
        models = response.json().get("data", [])
        logging.info(f"Available Models for API key: {[model['id'] for model in models]}")
    except requests.exceptions.RequestException as e:
        logging.error(f"Error retrieving available models: {e}")

def get_account_usage(session):
    """Optional function to get account usage details for the provided API key."""
    api_url = "https://api.openai.com/dashboard/billing/usage"

    try:
        response = session.get(api_url)
        response.raise_for_status()
        usage = response.json()
        logging.info(f"Account Usage Details: {usage}")
    except requests.exceptions.HTTPError as e:
        if response.status_code == 403:
            logging.warning("Access to billing/usage information is restricted for this API key.")
        else:
            logging.error(f"HTTP error occurred while retrieving account usage details: {e}")
    except requests.exceptions.RequestException as e:
        logging.error(f"Error retrieving account usage details: {e}")

def main():
    parser = argparse.ArgumentParser(description="Verify OpenAI API keys")
    parser.add_argument("api_key", type=str, help="The API key to verify")
    args = parser.parse_args()

    verify_api_key(args.api_key)

if __name__ == "__main__":
    main()

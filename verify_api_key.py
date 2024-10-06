import argparse
import requests
import re
import logging

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler()]
)

def verify_api_key(api_key):
    if not bool(re.match(r'^sk-[a-zA-Z0-9\-_]+$', api_key)):
        logging.error("API key format is invalid.")
        return False

    api_url = "https://api.openai.com/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "gpt-4",
        "messages": [
            {"role": "user", "content": "This is a test message to validate the API key."}
        ],
        "max_tokens": 1
    }

    try:
        response = requests.post(api_url, headers=headers, json=payload)
        response.raise_for_status()
        logging.debug("API key validation successful.")
        return True
    except requests.exceptions.RequestException as e:
        logging.error(f"Error during API key validation: {e}")
        return False

def main():
    parser = argparse.ArgumentParser(description="Verify OpenAI API keys")
    parser.add_argument("api_key", type=str, help="The API key to verify")
    args = parser.parse_args()

    verify_api_key(args.api_key)

if __name__ == "__main__":
    main()

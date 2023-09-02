import argparse
import requests

def verify_api_key(api_key):
    # Define the API endpoint URL
    api_url = "https://api.openai.com/v1/engines/davinci/completions"

    # Set up the headers with the API key
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    # Create a test request to check the API key
    try:
        response = requests.post(api_url, headers=headers)
        response.raise_for_status()  # Raise an exception if the request fails

        # If the request is successful, the API key is valid
        return True
    except requests.exceptions.RequestException:
        # If the request fails, the API key is invalid
        return False

def main():
    # Create a command-line argument parser
    parser = argparse.ArgumentParser(description="Verify OpenAI API keys")
    
    # Add an argument for the API key
    parser.add_argument("api_key", type=str, help="The API key to verify")
    
    # Parse the command-line arguments
    args = parser.parse_args()

    # Get the API key from the parsed arguments
    api_key = args.api_key

    # Verify the API key
    if verify_api_key(api_key):
        print("API key is valid.")
    else:
        print("API key is invalid.")

if __name__ == "__main__":
    main()

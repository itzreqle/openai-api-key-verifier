import argparse
import re
import logging
import json
import time
from urllib import request, error
from datetime import datetime, timezone, timedelta

# Setting up a unified logger
logger = logging.getLogger('OpenAIKeyVerifier')
logger.setLevel(logging.INFO)
console_handler = logging.StreamHandler()
formatter = logging.Formatter('[%(levelname)s] %(message)s')
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)

class OpenAIKeyVerificationError(Exception):
    pass

def verify_api_key(api_key):
    logger.debug("Verifying API key format...")
    if not bool(re.match(r'^sk-[\w-]+$', api_key)):
        logger.error("API key is invalid.")
        return False

    logger.debug("API key format is valid.")
    result = validate_api_key(api_key)
    return result

def make_api_request(url, api_key, method="GET", data=None):
    logger.debug(f"Making {method} request to {url}...")
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    req = request.Request(url, headers=headers, method=method)
    if data:
        req.data = json.dumps(data).encode('utf-8')
        logger.debug(f"Data payload: {req.data}")

    try:
        with request.urlopen(req) as response:
            logger.debug(f"Response status: {response.status}")
            response_data = json.loads(response.read())
            logger.debug(f"Response data: {response_data}")
            return response_data
    except error.HTTPError as e:
        response_status = e.code
        error_body = json.loads(e.read().decode())
        logger.debug(f"Response status: {response_status}")
        logger.debug(f"Response data: {error_body}")
        error_message = error_body.get('error', {}).get('message', str(e))
        
        if "You can find your API key" in error_message:
            error_message = error_message.split(". You can find your API key")[0]
        
        raise OpenAIKeyVerificationError(error_message)
    except error.URLError as e:
        logger.debug(f"URLError: {e.reason}")
        raise OpenAIKeyVerificationError(f"Connection error: {e.reason}")
    except json.JSONDecodeError:
        logger.debug("Failed to decode JSON response.")
        raise OpenAIKeyVerificationError("Invalid API response format.")

def validate_api_key(api_key):
    logger.debug("Validating API key...")
    try:
        make_api_request("https://api.openai.com/v1/models", api_key)
        logger.info("API key is valid.")
        return True
    except OpenAIKeyVerificationError:
        logger.error("API key is invalid.")
        return False

def check_model_access(api_key, model_name):
    logger.debug(f"Checking access for model: {model_name}...")
    try:
        model_url = f"https://api.openai.com/v1/models/{model_name}"
        make_api_request(model_url, api_key)
        logger.info(f"Access verified for model '{model_name}'.")
        return True
    except OpenAIKeyVerificationError as e:
        error_message = str(e).lower()
        if "no such model" in error_message:
            logger.error(f"Model '{model_name}' does not exist.")
        elif "insufficient_quota" in error_message:
            logger.error(f"Insufficient quota for model '{model_name}'.")
        elif "permission" in error_message or "not authorized" in error_message:
            logger.error(f"No permission to access model '{model_name}'.")
        else:
            logger.error(f"Could not access model '{model_name}': {e}")
        return False

def list_models(api_key):
    logger.debug("Listing available models...")
    try:
        response = make_api_request("https://api.openai.com/v1/models", api_key)
        models = response.get("data", [])
        logger.debug(f"Found {len(models)} models.")
        
        logger.info("\nAvailable Models:")
        for model in models:
            logger.info(f"• {model['id']}")
        return [model['id'] for model in models]
    except OpenAIKeyVerificationError as e:
        logger.error(f"Failed to list models: {e}")
        return []

def get_account_usage(api_key):
    logger.debug("Retrieving account usage...")
    try:
        now = datetime.now(timezone.utc)
        start_date = now.replace(day=1)
        end_date = now

        logger.debug(f"Getting usage data from {start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')}.")
        total_tokens_used = 0

        # Pricing per 1 million tokens
        input_cost_per_million = 0.15  # USD
        output_cost_per_million = 0.60  # USD

        current_date = start_date
        month_data = []

        while current_date <= end_date:
            date_str = current_date.strftime("%Y-%m-%d")
            url = f"https://api.openai.com/v1/usage?date={date_str}"
            retry = True

            while retry:
                try:
                    usage_data = make_api_request(url, api_key)
                    if usage_data and 'data' in usage_data:
                        month_data.append(usage_data)

                        input_tokens = sum(item.get('n_context_tokens_total', 0) for item in usage_data['data'])
                        output_tokens = sum(item.get('n_generated_tokens_total', 0) for item in usage_data['data'])
                        daily_tokens = input_tokens + output_tokens

                        input_cost = (input_tokens / 1_000_000) * input_cost_per_million
                        output_cost = (output_tokens / 1_000_000) * output_cost_per_million
                        daily_cost = input_cost + output_cost

                        logger.info(f"{date_str} | Input: {input_tokens:>8} · ${input_cost:>8.6f} | "
                                    f"Output: {output_tokens:>8} · ${output_cost:>8.6f} | "
                                    f"Total: {daily_tokens:>8} · ${daily_cost:>8.6f}")

                    retry = False  # Successful request, break the retry loop

                except OpenAIKeyVerificationError as e:
                    if "rate limit" in str(e).lower():
                        logger.warning(f"Rate limit reached, retrying...")
                        time.sleep(5)  # Wait for 5 seconds before retrying
                    else:
                        logger.error(f"Failed to get usage data for {date_str}: {e}")
                        retry = False  # Other errors shouldn't be retried

            current_date += timedelta(days=1)

        # Calculate total tokens and cost for the month
        input_tokens_month = sum(
            item.get('n_context_tokens_total', 0)
            for day_data in month_data
            for item in day_data['data']
        )
        output_tokens_month = sum(
            item.get('n_generated_tokens_total', 0)
            for day_data in month_data
            for item in day_data['data']
        )

        total_tokens_month = input_tokens_month + output_tokens_month
        total_input_cost = (input_tokens_month / 1_000_000) * input_cost_per_million
        total_output_cost = (output_tokens_month / 1_000_000) * output_cost_per_million
        total_cost = total_input_cost + total_output_cost

        logger.info(
            "\n" +
            "╔════════════════════════════╗\n"
            "║ MONTHLY SUMMARY            ║\n"
            "╠────────────────────────────╣\n"
            f"║ Input:  {input_tokens_month:<8} ${total_input_cost:<8.6f} ║\n"
            f"║ Output: {output_tokens_month:<8} ${total_output_cost:<8.6f} ║\n"
            "╠────────────────────────────╣\n"
            f"║ \033[1mTotal:  {total_tokens_month:<8} ${total_cost:<8.6f}\033[0m ║\n"
            "╚════════════════════════════╝\n" )

    except OpenAIKeyVerificationError as e:
        logger.error(f"Failed to get usage data: {e}")
        return None

def main():
    parser = argparse.ArgumentParser(description="Verify OpenAI API keys")
    parser.add_argument("api_key", type=str, help="The API key to verify")
    parser.add_argument("--check-model", type=str, help="Check access to a specific model (e.g., gpt-4)")
    parser.add_argument("--list-models", action="store_true", help="List all available models")
    parser.add_argument("--show-usage", action="store_true", help="Show account usage details")
    parser.add_argument("--debug", action="store_true", help="Enable debug logging")
    
    args = parser.parse_args()

    if args.debug:
        logger.setLevel(logging.DEBUG)

    logger.debug("Starting verification process...")
    try:
        if verify_api_key(args.api_key):
            if args.check_model:
                check_model_access(args.api_key, args.check_model)
            if args.list_models:
                list_models(args.api_key)
            if args.show_usage:
                get_account_usage(args.api_key)
        else:
            logger.debug("Exiting due to invalid API key.")
            exit(1)
    except KeyboardInterrupt:
        logger.info("\n⚠️ Verification cancelled by user.")
        logger.debug("Exiting due to KeyboardInterrupt.")
        exit(1)
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        logger.debug("Exception details:", exc_info=True)
        exit(1)
    logger.debug("Verification process completed.")

if __name__ == "__main__":
    main()

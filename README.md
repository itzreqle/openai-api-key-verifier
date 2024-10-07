# OpenAI API Key Verifier

This Python library allows you to verify the validity of an OpenAI API key by making a test request to the OpenAI API and checking the response status. It is a useful tool for both individual developers and platforms that use OpenAI's API to ensure API keys are working as expected before making actual API calls.

## Why Use This Library?

While you can verify an OpenAI API key by simply making an API call yourself, this library offers several benefits:

- **Convenience**: It provides an easy, reusable way to verify keys with a single function call, handling potential errors and logging them properly.
- **Model Access Verification**: Can determine if your key has access to specific models like GPT-4, which is a paid feature. This is particularly useful for open source tools that require GPT-4 access.
- **Rate Limit Check**: It provides additional options to get information about rate limits, available models, and account usage.
- **Integration for Open Source Tools**: If you're developing an open-source tool that allows users to provide their own OpenAI API key, this library makes it easier to validate those keys and verify model access without duplicating code.
- **Security and Consistency**: This library adds a layer of consistent validation for any OpenAI API key by using regex format validation followed by an actual API call.
- **Detailed Usage Analysis**: Provides comprehensive monthly token usage statistics with cost breakdowns for input and output tokens.

## Security and Transparency

- **Open Source**: The library is fully open source, and you can inspect the code yourself to ensure that it is secure. You can also compile it directly from the source if you prefer.
- **Minimal Data Handling**: The library only sends your API key directly to OpenAI's official endpoints to verify validity. It does not store, log, or send API keys to any third party.
- **No Data Farming**: The library is not intended to farm or steal API keys. It was created in response to the need for a reliable, easy way to validate keys and verify model access.

## Prerequisites

- Python 3: You can download it from [python.org](https://python.org)

## Installation

To install the OpenAI API Key Verifier library using pip, run:

```bash
pip3 install openai_api_key_verifier
```

## Usage

### Python Example

```python
from openai_api_key_verifier import verify_api_key, check_model_access, list_models, get_account_usage

# Replace with your actual API key
api_key = "your_actual_api_key_here"

# Verify if the API key is valid
is_valid = verify_api_key(api_key)

if is_valid:
    print("API key is valid!")
    
    # Check for GPT-4 access
    if check_model_access(api_key, "gpt-4"):
        print("This key has GPT-4 access!")
    
    # List all available models
    list_models(api_key)
    
    # Get usage statistics
    get_account_usage(api_key)
else:
    print("API key is invalid.")
```

### Command Line Usage

You can verify an API key directly from the command line with various options:

```bash
# Basic verification
python3 verify_openai_api_key YOUR_API_KEY

# Check model access
python3 verify_openai_api_key YOUR_API_KEY --check-model gpt-4

# List available models
python3 verify_openai_api_key YOUR_API_KEY --list-models

# Show usage statistics
python3 verify_openai_api_key YOUR_API_KEY --show-usage

# Enable debug logging
python3 verify_openai_api_key YOUR_API_KEY --debug
```

## Available Functions

- `verify_api_key(api_key)`: Checks the validity of the API key by making a minimal request to the OpenAI API.
- `check_model_access(api_key, model_name)`: Verifies if the key has access to a specific model.
- `list_models(api_key)`: Lists available models for the given API key.
- `get_account_usage(api_key)`: Retrieves detailed account usage statistics, including token counts and costs.

## Key Features

- **Enhanced Error Handling**: Better handling of rate limits and API errors with automatic retries.
- **Detailed Usage Statistics**: Monthly token usage breakdown with separate tracking for input and output tokens.
- **Cost Analysis**: Calculation of costs based on current OpenAI pricing for both input and output tokens.
- **Debug Mode**: Additional logging options for troubleshooting with the `--debug` flag.
- **Improved Console Output**: Better formatted console output with clear visual indicators for success and failure.

## Contributing

If you'd like to contribute to this project, please fork the repository and create a pull request with your changes. We welcome feedback and improvements from the community to make this tool more useful.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
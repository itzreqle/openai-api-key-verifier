# OpenAI API Key Verifier

This Python library allows you to verify the validity of an OpenAI API key by making a test request to the OpenAI GPT-3 API and checking the response status. It is a useful tool to ensure that your API keys are working correctly.

## Prerequisites

Before you can use this library, make sure you have the following prerequisites installed:

- Python 3: You can download it from [python.org](https://www.python.org/downloads/).

## Installation

You can install the OpenAI API Key Verifier library using pip:

```bash
pip install openai_api_key_verifier
```

## Usage

To verify an OpenAI API key, follow these steps:

1. Import the library in your Python script.
2. Use the `verify_api_key` function to check the validity of the API key.

Here's an example:

```python
from openai_api_key_verifier import verify_api_key

api_key = "YOUR_API_KEY"
is_valid = verify_api_key(api_key)

if is_valid:
    print("API key is valid!")
else:
    print("API key is invalid.")
```

Replace `YOUR_API_KEY` with the actual OpenAI API key you want to check.

## Example

To run a complete example:

```python
from openai_api_key_verifier import verify_api_key

# Replace with your actual API key
api_key = "your_actual_api_key_here"

is_valid = verify_api_key(api_key)

if is_valid:
    print("API key is valid!")
else:
    print("API key is invalid.")
```

If the program consistently reports that the API key is invalid, there could be several reasons for this:

* **Incorrect API Key**: Ensure you are providing the correct OpenAI API key.
* **Expired or Revoked Key**: Check the status of your API key in your OpenAI account dashboard.
* **Network Issues**: Make sure your computer has a working internet connection.
* **Firewall or Proxy Issues**: Ensure your network configurations allow requests to OpenAI's servers.
* **Rate Limits**: Verify that you haven't exceeded OpenAI's API rate limits.
* **OpenAI Service Status**: Check OpenAI's status page for any service disruptions.
* **Script Issues**: Test the script with a known working API key to verify its functionality.

If you've confirmed that your API key is correct and not expired, and you're still encountering issues, it's a good idea to contact OpenAI support for further assistance.

## Contributing

If you'd like to contribute to this project, please fork the repository and create a pull request with your changes.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
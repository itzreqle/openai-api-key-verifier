# OpenAI API Key Verifier

This Python script allows you to verify the validity of an OpenAI API key by making a test request to the OpenAI GPT-3 API and checking the response status. It is a useful tool to ensure that your API keys are working correctly.

## Prerequisites

Before you can use this program, make sure you have the following prerequisites installed:

- Python 3: You can download it from [python.org](https://www.python.org/downloads/).

## Installation

1. Clone or download this repository to your local machine.

```bash
git clone https://github.com/itzreqle/openai-api-key-verifier.git
```

2. Navigate to the project directory.

```bash
cd openai-api-key-verifier
```

3. Install the required Python packages using pip.

```bash
pip install -r requirements.txt
```

## Usage

To verify an OpenAI API key, follow these steps:

1. Open a terminal or command prompt.

2. Navigate to the directory where you downloaded or cloned this repository.

3. Run the script with the API key as an argument:

```bash
python verify_api_key.py YOUR_API_KEY
```

Replace `YOUR_API_KEY` with the actual OpenAI API key you want to check.

4. The script will send a test request to the OpenAI GPT-3 API and check if the API key is valid. It will then display a message indicating whether the key is valid or invalid.

## Example

Here's an example of how to use the script:

```bash
python verify_api_key.py your_actual_api_key_here
```
If the program consistently reports that the API key is invalid, there could be several reasons for this:

    Incorrect API Key: Make sure you are providing the correct OpenAI API key. The API key should be a long string of letters and numbers, and it should be copied and pasted accurately into the command line.

    Expired or Revoked Key: If the API key has expired or has been revoked by OpenAI, it will be considered invalid. Check the status of your API key in your OpenAI account dashboard.

    Network Issues: Ensure that your computer has a working internet connection. The script needs to make a network request to OpenAI's servers to validate the API key.

    Firewall or Proxy Issues: If you're behind a corporate firewall or using a proxy server, it may be blocking the script's requests. Make sure that the necessary network configurations are in place.

    Rate Limits: OpenAI imposes rate limits on API requests. If you have exceeded the rate limits, it may temporarily block your requests, leading to an "invalid" response. Check OpenAI's documentation for rate limit details and ensure you're not exceeding them.

    OpenAI Service Status: Sometimes, OpenAI services can experience downtime or issues. Check OpenAI's status page or their official communication channels for any service disruptions.

    Script Issues: Ensure that the script itself is working correctly, and there are no typos or errors in the code. You can also test the script with a known working API key to verify its functionality.

If you've confirmed that your API key is correct and not expired, and you're still encountering issues, it's a good idea to contact OpenAI support for further assistance. They can help you troubleshoot and identify any specific issues with your account or API key.

## Contributing

If you'd like to contribute to this project, please fork the repository and create a pull request with your changes.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

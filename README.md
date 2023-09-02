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

## Contributing

If you'd like to contribute to this project, please fork the repository and create a pull request with your changes.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

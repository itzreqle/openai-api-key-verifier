from setuptools import setup, find_packages

setup(
    name='openai_api_key_verifier',
    version='0.1.1',
    author='Marcus Deacey',
    author_email='marcusdeacey@duck.com',  # Replace with your email
    description='A Python library to verify the validity of OpenAI API GPT-4 keys.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/mdeacey/openai-api-key-verifier',  # Your repository URL
    packages=find_packages(),
    install_requires=[
        'requests',
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',  # Adjust the Python version requirement as needed
)
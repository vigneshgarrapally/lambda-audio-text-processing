# Lambda Functions

**This repository contains the source code for three Lambda functions that can be used to transcribe audio, generate text from speech, and process text using a large language model.**

The Lambda functions are:

1. transcription.py: This function takes as its input a URL of a .wav file stored in S3 and returns the text of the transcript created by a third-party API (either OpenAI Whisper or Deepgram Nova).

2. text_to_speech.py: This function takes as its input some text and returns the URL of an audio file generated by a third-party API (either Google Cloud Text-to-Speech or ElevenLabs Text to Speech).

3. llm_text_processing.py: This function takes as its input some text to process, as well as system prompts, and returns the response from a third-party API (OpenAI ChatGPT).

The repository also includes a layers directory that contains a .zip file with the LangChain layer that is used by the llm_text_processing.py function.

> More information about the functions and how to deploy and use them can be found in the docs folder.

## Initial Setup

1. Clone the repository to your local machine.
2. Duplicate the .env.example file and rename it to .env.
3. In the .env file, add your API keys for the third-party APIs that you will be using.
4. Go to respective Lambda function folder and read the readme file for deployment instructions.

> Note: [Notebooks](./notebooks) folder contains various notebooks that are helpful to understand the code and test the Lambda functions.

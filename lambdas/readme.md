# Lambda Functions

This folder contains code for the Lambda functions used in the project. There are three Lambda functions in this project:

1. [Transcription Lambda](./lambda1/): This Lambda will take as its input a URL of a .wav file stored in S3. It will call a specified third party API for transcription (either OpenAI Whisper or Deepgram Nova), choosing which one depending on a parameter passed in. Then it will return the text of the transcript created by the third party API.

2. [Text To Speech Lambda](./lambda2/): This Lambda will take as its input some text. It will call a specified third party API for text to speech (either Google Cloud Text-to-Speech or ElevenLabs Text to Speech), choosing which one depending on a parameter passed in. Then it will store the generated audio file in a specified S3 bucket and return the URL of that S3 file.

3. [LLM Text Processing Lambda](./lambda3/): This Lambda will take as its input some text to process, as well as system prompts provided by user. It will use LangChain (via a Layer) to call OpenAI ChatGPT for LLM text processing.Then it will return the ChatGPT response as text.

Please refer to the README files in the respective folders for more details about the Lambda functions.

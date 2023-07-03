# Given Task Description

Implement three different Lambda functions using Python: Transcription, Text to Speech, and LLM Text Processing. Each Lambda will call one or two third-party APIs as specified below and return the results.

## Description of Work to be Completed

The engineer will write Python code (which will run in three distinct AWS Lambdas) that are invoked from time to time by pMD’s application. Each Lambda function has different inputs and outputs, and serves a different purpose.

### Transcription Lambda

This Lambda will take as its input a URL of a .wav file stored in S3. It will call a
specified third party API for transcription (either OpenAI Whisper or Deepgram Nova), choosing which one depending on a parameter passed in. Then it will return the text of the transcript created by the third party API.

### Text to Speech Lambda

This Lambda will take as its input some text. It will call a specified third party API
for text to speech (either Google Cloud Text-to-Speech or ElevenLabs Text to Speech), choosing which one depending on a parameter passed in. Then it will store the generated audio file in a specified S3 bucket and return the URL of that S3 file.

### LLM Text Processing Lambda

This Lambda will take as its input some text to process, as well as system prompts provided by pMD. It will use LangChain (via a Layer) to call a specified third party API (OpenAI ChatGPT) for LLM text processing. It should use LangChain LLM mode, not Chat mode. Then it will return the ChatRPT response as text.

# Transcription Lambda Function

## Description

This folder contains the code for the transcription lambda.This Lambda will take as its input a URL of a .wav file stored in S3. It will call a specified third party API for transcription (either OpenAI Whisper or Deepgram Nova), choosing which one depending on a parameter passed in. Then it will return the text of the transcript created by the third party API.

## Functionality

1. The function is triggered by an HTTP request, which includes the S3 URL of the audio file to be transcribed and the name of the API to use for transcription.
2. Supported APIs are OpenAI Whisper (`whisper`) and Deepgram Nova (`deepgram`).
3. The Lambda function assumes that the audio file is in .wav format. If not, it will return an error.
4. The Lambda function assumes that the url received in the HTTP request is a valid S3 Object URL that lambda has access to. If not, it will return an error stating permission denied.
5. If no API is specified, the Lambda will default to OpenAI Whisper.
6. The Lambda will return the text of the transcript created by the third party API.

## Deployment Steps

1. Create a new Lambda function in the AWS console.
2. Upload the code in this folder to the Lambda function.
3. Upload the [layer](./layers/transcriptionlayer.zip) in the `layer` folder to the Lambda function and add it as a layer.
4. Make sure the Lambda function has access to the S3 bucket where the audio files are stored by adding the appropriate permissions to the execution role of the Lambda function.
5. Update the required environment variables in the Lambda function.
6. Update the Resource values as shown in the [SAM template](./transcriptionlambda.yaml).
7. Deploy the Lambda function

## Environment Variables

The following environment variables are required for the Lambda function to work:

1. `DEEPGRAM_API_KEY`: The API key for the Deepgram API.
2. `OPENAI_API_KEY`: The API key for the OpenAI API.

## Resource Values

Following are the values that need to be updated in the Lambda function. Feel free to change the values as per your requirements.

1. `MemorySize` : 128
2. `Timeout` : 123
3. `Runtime` : python3.10

## Test Example (Python)

```python
import boto3
import json

payload = {
    "body": json.dumps(
        {
            "s3_audio_url": "https://pmd-lambda-outputs.s3.amazonaws.com/audio_files/sample_audio.wav",
            "api": "whisper",
        }
    )
}

client = boto3.client("lambda")
response = client.invoke(
    FunctionName="transcriptionlambda",
    InvocationType="RequestResponse",
    Payload=json.dumps(payload),
)
response = json.loads(response["Payload"].read())
print(response)
```

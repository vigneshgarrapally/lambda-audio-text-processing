import json
import os
import boto3
from elevenlabs import generate, set_api_key
import google.cloud.texttospeech as tts
import datetime
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def upload_file_to_s3(
    local_file_path, bucket_name, s3_file_key=None, buffered_data=None
):
    """
    Uploads a file to Amazon S3.

    Parameters:
    - local_file_path (str): The local file path of the file to upload.
    - bucket_name (str): The name of the S3 bucket to upload the file to.
    - s3_file_key (str, optional): The S3 file key (path) where the file will be stored. If not provided,
                                  the file will be stored in the root of the bucket with the same name as the
                                  local file.
    - buffered_data (bytes, optional): The buffered data to upload instead of using a local file. If provided,
                                       local_file_path will be ignored.

    Returns:
    - The S3 URL of the uploaded file.
    """
    s3 = boto3.client(
        "s3",
        # aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),
        # aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY"),
        # region_name=os.environ.get("AWS_REGION"),
    )
    if buffered_data:
        response = s3.put_object(
            Bucket=bucket_name, Key=s3_file_key, Body=buffered_data
        )
    else:
        # If s3_file_key is not provided, use the local file name as the key
        if s3_file_key is None:
            s3_file_key = local_file_path.split("/")[-1]

        # Upload the file to S3
        with open(local_file_path, "rb") as file:
            response = s3.put_object(Bucket=bucket_name, Key=s3_file_key, Body=file)

    # Get the URL of the uploaded file
    s3_url = f"https://{bucket_name}.s3.amazonaws.com/{s3_file_key}"
    return s3_url


def text_to_wav(text: str, filename: str):
    voice_name = "en-US-Wavenet-F"
    api_key_string = os.getenv("GOOGLE_CLOUD_TEXT_TO_SPEECH_API_KEY")
    language_code = "-".join(voice_name.split("-")[:2])
    text_input = tts.SynthesisInput(text=text)
    voice_params = tts.VoiceSelectionParams(
        language_code=language_code, name=voice_name
    )
    audio_config = tts.AudioConfig(audio_encoding=tts.AudioEncoding.LINEAR16)

    client = tts.TextToSpeechClient(client_options={"api_key": api_key_string})
    response = client.synthesize_speech(
        input=text_input,
        voice=voice_params,
        audio_config=audio_config,
    )
    with open(filename, "wb") as out:
        out.write(response.audio_content)
        logging.info(f'Audio content written to file "{filename}"')


def lambda_handler(event, context):
    body = json.loads(event.get("body", "{}"))
    logger.info(body)
    # get text from body
    text = body.get("text", "")
    api = body.get("api", "google")
    logger.info("Text: " + text)
    logger.info("API: " + api)
    filename = "/tmp/" + datetime.datetime.now().strftime("%Y-%m-%d_%H%M%S") + ".wav"
    logger.info("Filename: " + filename)
    if api == "elevenlabs":
        set_api_key(os.getenv("ELEVENLABS_API_KEY"))
        audio = generate(
            text=text,
            voice="Bella",
            model="eleven_monolingual_v1",
        )
        # save audio to file
        with open(filename, "wb") as audio_file:
            audio_file.write(audio)
        # upload file to S3
    elif api == "google":
        text_to_wav(text, filename)
    else:
        logger.info("API not supported. Please use elevenlabs or google")
        return {
            "statusCode": 400,
            "body": "API not supported. Please use elevenlabs or google",
        }
    # invoke text to speech api and generate audio
    # upload audio to s3
    s3_audio_url = upload_file_to_s3(filename, os.getenv("AWS_BUCKET_NAME"))
    logger.info("S3 URL: " + s3_audio_url)
    result = {"statusCode": 200, "body": json.dumps(s3_audio_url)}
    return result

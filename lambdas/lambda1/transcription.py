# import all required modules
import json
import os
from deepgram import Deepgram
import openai
import boto3


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


def download_file_from_s3(s3_url):
    """
    Downloads a file from an S3 URL to a local file.

    Parameters:
    - s3_url (str): The URL of the file in S3, e.g., 'https://your-bucket-name.s3.amazonaws.com/your-file.wav'.
    - local_file_path (str): The local file path where the downloaded file will be stored.

    Returns:
    - True if the download is successful, False otherwise.
    """
    s3 = boto3.client(
        "s3",
        # region_name=os.environ.get("AWS_REGION"),
        # aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),
        # aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY"),
    )

    # Extract the bucket name and object key from the S3 URL
    try:
        bucket_name = s3_url.split("//")[1].split(".")[0]
        object_key = s3_url.split(bucket_name + ".s3.amazonaws.com/")[1]
    except Exception as e:
        print("Error parsing the S3 URL:", e)
        return False
    print(f"Bucket name: {bucket_name}, Object key: {object_key}")

    filename = object_key.split("/")[-1]
    # add /tmp/ to the filename to download to the /tmp/ folder
    filename = f"/tmp/{filename}"
    print(f"Filename: {filename}")
    # # check if /tmp/ folder exists
    # if not os.path.exists("/tmp/"):
    #     os.makedirs("/tmp/")
    # Download the file from S3
    try:
        s3.download_file(bucket_name, object_key, filename)
        print(f"File downloaded successfully to {filename}")
        return filename
    except Exception as e:
        print("Error downloading the file:", e)
        return None


async def deepgram_transcribe(audio):
    # get deepgram api key
    deepgram_api_key = os.environ.get("DEEPGRAM_API_KEY")
    # create deepgram client
    dg_client = Deepgram(deepgram_api_key)
    options = {"punctuate": True, "model": "general", "tier": "enhanced"}
    source = {"buffer": audio, "mimetype": "audio/wav"}
    response = await dg_client.transcription.prerecorded(source, options)
    transcription = response["results"]["channels"][0]["alternatives"][0]["transcript"]
    return transcription


def lambda_handler(event, context):
    body = json.loads(event.get("body", "{}"))
    print(body)
    # get s3 audio url from body
    s3_audio_url = body.get("s3_audio_url", "")
    print("Aduio URL: ", s3_audio_url)
    # check if s3 audio url ends with .wav
    if not s3_audio_url.endswith(".wav"):
        return {"statusCode": 400, "body": json.dumps("Audio file must be .wav")}
    # get name of api to use to generate transcription. Supported apis are deepgram and elevenlabs
    api = body.get("api_name", "whisper")
    print("API to use for transcription: ", api)
    # download audio file from s3
    filename = download_file_from_s3(s3_audio_url)
    if filename is None:
        return {"statusCode": 400, "body": json.dumps("Error downloading audio file")}
    with open(filename, "rb") as audio:
        if api == "deepgram":
            # get deepgram transcription
            transcription = deepgram_transcribe(audio)

        elif api == "whisper":
            # get whisper api key
            openai.api_key = os.getenv("OPENAI_API_KEY")
            transcript = openai.Audio.transcribe("whisper-1", audio)
            transcription = transcript.text
        else:
            return {"statusCode": 400, "body": json.dumps("Invalid api name")}
    print("Transcription: ", transcription)
    return {"statusCode": 200, "body": json.dumps(transcription)}

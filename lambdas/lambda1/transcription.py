import json


def lambda_handler(event, context):
    body = json.loads(event.get("body", "{}"))
    print(body)
    # get s3 audio url from body
    s3_audio_url = body.get("s3_audio_url", "")
    # invoke transcription api and get transcription
    transcription = "Hello from Lambda!"
    result = {"statusCode": 200, "body": json.dumps(transcription)}
    return result

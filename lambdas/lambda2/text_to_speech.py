import json

def lambda_handler(event, context):
    body=json.loads(event.get("body", "{}"))
    print(body)
    #get s3 audio url from body
    text=body.get("text", "")
    #invoke text to speech api and generate audio
    #upload audio to s3
    s3_audio_url="you will see the s3 url here"
    result={
        "statusCode": 200,
        "body": json.dumps(s3_audio_url)
    }
    return result
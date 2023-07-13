# local testing
import json
import sys

from dotenv import load_dotenv

load_dotenv()
sys.path.append("../lambdas/lambda1")
from transcription import lambda_handler


payload = {
    "body": json.dumps(
        {
            "s3_audio_url": "https://pmd-lambda-outputs.s3.amazonaws.com/audio_files/sample_audio.wav",
            "api_name": "deepgram",
        }
    )
}

response = lambda_handler(payload, None)
print(response)

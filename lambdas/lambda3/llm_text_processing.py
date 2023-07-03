import json

def lambda_handler(event, context):
    body = json.loads(event.get("body", "{}"))
    print(body)
    text_to_process = body.get("text", "")
    prompt = body.get("prompt", "")
    chatgpt_response = "Here you will see the chatgpt response for the text and prompt you sent"
    result = {
        "statusCode": 200,
        "body": json.dumps(chatgpt_response)
    }
    return result

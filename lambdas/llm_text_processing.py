import json

def lambda_handler(event, context):
    body = json.loads(event.get("body", "{}"))
    print(body)
    answer = "Hello from Lambda!"
    result={
        "statusCode": 200,
        "body": json.dumps(answer)
    }
    return result

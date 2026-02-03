import os
import json
import boto3

dynamodb = boto3.resource("dynamodb")
TABLE_NAME = os.environ["TABLE_NAME"]
PK_VALUE = os.environ["PK_VALUE"]

table = dynamodb.Table(TABLE_NAME)

def lambda_handler(event, context):
    # increment atomically
    resp = table.update_item(
        Key={"pk": PK_VALUE},
        UpdateExpression="ADD #c :inc",
        ExpressionAttributeNames={"#c": "count"},
        ExpressionAttributeValues={":inc": 1},
        ReturnValues="UPDATED_NEW",
    )

    count = resp["Attributes"]["count"]

    # Function URL expects CORS headers if called from browser
    return {
        "statusCode": 200,
        "headers": {
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "GET,OPTIONS",
            "Access-Control-Allow-Headers": "content-type",
            "content-type": "text/plain"
        },
        "body": str(count),
    }

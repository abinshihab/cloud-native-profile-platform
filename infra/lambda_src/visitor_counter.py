import json
import boto3

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table("visitor_counter_v2")

def lambda_handler(event, context):
    response = table.update_item(
        Key={"pk": "site#awsbenshehab"},
        UpdateExpression="ADD #count :inc",
        ExpressionAttributeNames={"#count": "count"},
        ExpressionAttributeValues={":inc": 1},
        ReturnValues="UPDATED_NEW"
    )

    count = int(response["Attributes"]["count"])

    return {
        "statusCode": 200,
        "headers": {
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "GET,OPTIONS",
            "Access-Control-Allow-Headers": "Content-Type"
        },
        "body": str(count)
    }

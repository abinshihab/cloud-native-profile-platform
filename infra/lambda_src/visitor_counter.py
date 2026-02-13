import boto3
import os
import time

dynamodb = boto3.resource("dynamodb")

counter_table = dynamodb.Table(os.environ["COUNTER_TABLE"])
visitors_table = dynamodb.Table(os.environ["VISITORS_TABLE"])

pk_value = os.environ["PK_VALUE"]

def lambda_handler(event, context):

    try:
        ip = event["requestContext"]["http"]["sourceIp"]
    except KeyError:
        ip = event["requestContext"]["identity"]["sourceIp"]

    now = int(time.time())
    ttl = now + 86400  # 24h

    try:
        visitors_table.put_item(
            Item={
                "pk": ip,
                "ttl": ttl
            },
            ConditionExpression="attribute_not_exists(pk)"
        )

        response = counter_table.update_item(
            Key={"pk": pk_value},
            UpdateExpression="ADD #count :inc",
            ExpressionAttributeNames={"#count": "count"},
            ExpressionAttributeValues={":inc": 1},
            ReturnValues="UPDATED_NEW"
        )

        count = int(response["Attributes"]["count"])

    except Exception:
        response = counter_table.get_item(
            Key={"pk": pk_value}
        )
        count = int(response["Item"]["count"])

    return {
        "statusCode": 200,
        "headers": {
            "Access-Control-Allow-Origin": "*"
        },
        "body": str(count)
    }

import boto3
import os
import time
from botocore.exceptions import ClientError

dynamodb = boto3.resource("dynamodb")

counter_table = dynamodb.Table(os.environ["COUNTER_TABLE"])
visitors_table = dynamodb.Table(os.environ["VISITORS_TABLE"])
pk_value = os.environ["PK_VALUE"]

CORS_HEADERS = {
    "Access-Control-Allow-Origin": "*",
    "Access-Control-Allow-Methods": "GET,OPTIONS",
    "Access-Control-Allow-Headers": "Content-Type",
    "Content-Type": "application/json",
}

def get_source_ip(event):
    # HTTP API v2
    rc = event.get("requestContext", {})
    http = rc.get("http")
    if http and "sourceIp" in http:
        return http["sourceIp"]
    # REST API v1 fallback
    identity = rc.get("identity", {})
    return identity.get("sourceIp", "unknown")

def lambda_handler(event, context):
    # Handle preflight (optional but nice)
    if event.get("requestContext", {}).get("http", {}).get("method") == "OPTIONS":
        return {"statusCode": 204, "headers": CORS_HEADERS, "body": ""}

    ip = get_source_ip(event)
    now = int(time.time())
    ttl = now + 86400  # 24h

    counted = False

    # 1) Try to record unique visitor for 24h
    try:
        visitors_table.put_item(
            Item={"pk": ip, "ttl": ttl},
            ConditionExpression="attribute_not_exists(pk)"
        )
        counted = True
    except ClientError as e:
        # Only ignore the "already exists" case; anything else is real trouble
        if e.response["Error"]["Code"] != "ConditionalCheckFailedException":
            raise

    # 2) Increment counter only if first visit in 24h
    if counted:
        resp = counter_table.update_item(
            Key={"pk": pk_value},
            UpdateExpression="ADD #count :inc",
            ExpressionAttributeNames={"#count": "count"},
            ExpressionAttributeValues={":inc": 1},
            ReturnValues="UPDATED_NEW"
        )
        count = int(resp["Attributes"]["count"])
    else:
        resp = counter_table.get_item(Key={"pk": pk_value})
        count = int(resp.get("Item", {}).get("count", 0))

    return {
        "statusCode": 200,
        "headers": CORS_HEADERS,
        "body": f'{{"visits":{count},"counted":{str(counted).lower()}}}'
    }
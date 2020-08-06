import boto3
import json
import os


def lambda_handler(event, context):
    dynamodb = boto3.resource("dynamodb")
    ddbTableName = os.environ["databaseName"]
    table = dynamodb.Table(ddbTableName)

    # Atomic update item in table or add if doesn't exist
    ddbResponse = table.update_item(
        Key={"page": "BansiResume"},
        UpdateExpression="ADD NumOfViews :inc",
        ExpressionAttributeValues={":inc": 1},
        ReturnValues="UPDATED_NEW",
    )

    # Format dynamodb response into variable visitorCount
    responseBody = json.dumps(
        {"visitorCount": int(float(ddbResponse["Attributes"]["NumOfViews"]))}
    )

    # Create api response object
    apiResponse = {
        "isBase64Encoded": False,
        "statusCode": 200,
        "body": responseBody,
        "headers": {
            "Access-Control-Allow-Headers": "Content-Type,X-Amz-Date,Authorization,X-Api-Key,x-requested-with",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "GET,OPTIONS",
        },
    }

    return apiResponse

import json
import boto3
import os


def lambda_handler(event, context):
    '''
    Updates the DynamoDB entry with with the website name as the primary key by one
    If the key exists, it increases by one
    If it does not exist, it creates it and adds one
    '''

    dynamodb = boto3.client('dynamodb')
    ddTableName=os.environ['databaseName']
    table = dynamodb.Table(ddTableName)

    ddResponse = table.update_item(
        Key={
            'id': {'S': "bansimendapara.com"}
        },
        UpdateExpression='ADD visitors :inc',
        ExpressionAttributeValues={
            ':inc': {'N': '1'}
        },
        ReturnValues="UPDATED_NEW"
    )

    # Format dynamodb response into variable visitorCount
    responseBody = json.dumps(
        {"visitorCount": int(float(ddResponse['Attributes']['visitors']['N'])}
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

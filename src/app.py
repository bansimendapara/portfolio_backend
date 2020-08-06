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

    response = table.update_item(
        Key={"page": "BansiResume"},
        UpdateExpression="ADD NumOfViews :inc",
        ExpressionAttributeValues={":inc": 1},
        ReturnValues="UPDATED_NEW",
    )

    return {
        "statusCode": 200,
        'headers': {
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
        },
        "body": json.dumps({"visitorCount": int(response["Attributes"]["NumOfViews"])})
    }

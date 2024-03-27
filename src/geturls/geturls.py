import json
import boto3
from boto3.dynamodb.conditions import Key
import os
from decimal import Decimal

tableName = os.environ.get('URLSHORTNERTABLE_TABLE_NAME')
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(tableName)
domainNameParam = os.environ.get('DOMAIN_NAME_PARAM')

def decimal_default(val):
    if isinstance(val, Decimal):
        return int(val)
    raise TypeError

def handler(event, context):
    
    basePath = event["headers"]["host"]
    domainName = event["requestContext"]["domainName"]
    stage = event["requestContext"]["stage"]
    email = event['requestContext']['authorizer']['jwt']['claims']['email']
    try:
        response = table.query(
            IndexName="createdByIndex",
            KeyConditionExpression=Key('createdBy').eq(email)
        )

        items = response['Items']

        # extract specific fields
        filterdItems = [
            {
                'id': item['id'],
                'shortCode': item['shortCode'],
                'createdAt': item['createdAt'],
                'originalUrl': item['originalUrl'],
                'clicks': item['clicks'],   
                'shortUrl': f'https://{basePath}/{stage}/{item["shortCode"]}' if domainNameParam not in domainName else  f'https://{basePath}/{item["shortCode"]}'            
            }
            for item in items
        ]

        return {
            'statusCode': 200,
            'body': json.dumps(filterdItems, default=decimal_default),
            'headers' : {
                'Content-Type': 'application/json'
            }
        }
    except Exception as e:
        print(e)
        return {
            'statusCode': 404,
            'body': json.dumps({'message': 'error getting values'}),
            'headers' : {
                'Content-Type': 'application/json'
            }
        }

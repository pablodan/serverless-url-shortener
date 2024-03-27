import json
import boto3
from boto3.dynamodb.conditions import Key
import os


tableName = os.environ.get('URLSHORTNERTABLE_TABLE_NAME')
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(tableName)


def handler(event, context):

    try:
        shortCode = event['pathParameters']['short_code']
        response = table.query(
            IndexName = 'UniqueKeyIndex',
            KeyConditionExpression=Key('shortCode').eq(shortCode)
        )
        print(f'{response}')
        items = response.get('Items', [])
        print(items)
        if items:
            item = items[0]
            # here we can get individual key
            origInalUrl = item['originalUrl']
            primaryKey = {'id': item.get('id')}

            # increment the number of clicks, each time a url is visited
            table.update_item(
                Key = primaryKey,
                UpdateExpression="ADD clicks :increment",
                ExpressionAttributeValues={
                    ':increment': 1
                },
            )

        return {
            'statusCode': 302,
            'headers': {
            'Location': origInalUrl
            },
        }
    except Exception as e:
        print(e)
        return {
            'statusCode': 404,
            'body': 'No matching URL'
        }





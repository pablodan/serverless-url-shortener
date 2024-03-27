import json
import boto3
import os
from boto3.dynamodb.conditions import Attr


tableName = os.environ.get('URLSHORTNERTABLE_TABLE_NAME')
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(tableName)

def handler(event, context):

    try:
        email = event['requestContext']['authorizer']['jwt']['claims']['email']

        # delete/{id}
        recordId = event['pathParameters']['id']

        # delete our matching id
        response = table.delete_item(
            Key = {
                'id': recordId
            },
            ConditionExpression=Attr('createdBy').eq(email)
        )
        print(f'response for debugging: {response}')

        return {
            'statusCode': 201,
            'body': json.dumps({'message': 'Sucessfully delete record'}),
            'headers': {'Content-Type': 'application/json'}
        }
    
    except table.meta.client.exceptions.ConditionalCheckFailedException:

        return {
            'statusCode': 403,
            'body': json.dumps({'message': 'Not authorized to delete this url'}),
            'headers': {'Content-Type': 'application/json'}
        }
    
    except KeyError:
        return {
            'statusCode': 400,
            'body': json.dumps({'message': 'failed to delete record'}),
            'headers': {'Content-Type': 'application/json'}
        }
 


import json
import os
import boto3
import uuid
import random
import string
from datetime import datetime, timedelta

tableName = os.environ.get('URLSHORTNERTABLE_TABLE_NAME')
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(tableName)
domainNameParam = os.environ.get('DOMAIN_NAME_PARAM')

# later one, input checks to make sure this string isnt already in database
def generate_short_code(url, length=6):
    char_pool = string.ascii_uppercase + string.ascii_lowercase + string.digits
    return ''.join(random.sample(char_pool, length))
    

def handler(event, context):
    print(event)
    body= json.loads(event["body"])
    print(f'Body from event: {body}')
    originalUrl = body.get('originalUrl')
    domainName = event["requestContext"]["domainName"]
    stage = event["requestContext"]["stage"]
    shortUrlResponse = generate_short_code(originalUrl)

    email = event['requestContext']['authorizer']['jwt']['claims']['email']
    if domainNameParam not in domainName:
        print('match')
        shortUrl = f'https://{event["headers"]["host"]}/{stage}/{shortUrlResponse}'
    else: # prod with custom domain
        print('custom domain')
        shortUrl = f'https://{event["headers"]["host"]}/{shortUrlResponse}'

    data = {
        'id': str(uuid.uuid4()),
        'createdBy': email,
        'originalUrl': originalUrl,
        'shortCode': shortUrlResponse,
        'createdAt': datetime.utcnow().isoformat(),
        'clicks': 0
    }

    try:
        table.put_item(Item=data)
        return {
            'statusCode': 201,
            'body': json.dumps({
                'shortUrl': shortUrl
            }),
            'headers': {
                'Content-Type': 'application/json'
            }
        }
    except Exception as e:
        response = {
            'statusCode': 403,
            'body': json.dumps({"message": "error saving data"})
        }




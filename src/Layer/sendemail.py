import boto3
import os
from botocore.exceptions import ClientError

region = os.environ.get('EMAIL_REGION')
ses_client = boto3.client('ses', region_name=region)

def sendEmail(sender_email, recipient_address, subject, message):
    if not sender_email:
        raise ValueError("Sender email address needed")
    
    try:
        response = ses_client.send_email(
            Source=sender_email,
            Destination = {
                'ToAddresses': [
                    recipient_address,
                ]
            },
            Message={
                'Subject': {
                    'Data': subject
                },
                'Body': {
                    'Text':{
                        'Data': message
                    }
                }
            }
        )
        return response
    except ClientError as e:
        print(e.response['Error']['Message'])
        return None
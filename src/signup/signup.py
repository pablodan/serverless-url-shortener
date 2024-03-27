import json
import secretmanager
import firebase_admin
from firebase_admin import credentials, auth, exceptions
import os
import logging
import boto3
from datetime import datetime
from sendemail import sendEmail

logger = logging.getLogger()
logger.setLevel(logging.INFO)

tableName = os.environ.get('USERTABLE_TABLE_NAME')
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(tableName)
secretName = os.environ.get('SECRET_NAME')
senderEmail = os.environ.get('SENDER_EMAIL')

if not firebase_admin._apps:
    firebase_creds = secretmanager.get_secret(secretName)
    # web_api_key = firebase_creds['web_api_key']

    # initalize firebase admin
    cred = credentials.Certificate(firebase_creds)
    firebase_admin.initialize_app(cred)

def add_user(user_id, email):
    try:
        response = table.put_item(
            Item={
                'id': user_id,
                'email': email,
                'createdAt': datetime.now().isoformat()
            }
        )
    except Exception as e:
        logger.error(f'Error creating user {e}')

def register_user(email, password, secretName):
    try:
        user = auth.create_user(email=email, password=password)
        logger.info(f'User Created: {user}')
        verficationLink = auth.generate_email_verification_link(email, action_code_settings=None, app=None)
        logger.info(f'Verification link: {verficationLink}')
        emailMessage = f'To complete your registartion, please click the link included: {verficationLink}'
        emailResponse = sendEmail(senderEmail, email, "Verify your email", emailMessage)
        logger.info(f'Email Response: {emailResponse}')
        return {
            "message": "Successfully created user",
            "user_id": user.uid,
            "verficationLink": verficationLink    
        }
    except auth.EmailAlreadyExistsError:
        return {"error": "User already exists"}
    
    except exceptions.FirebaseError as fe:
        return {"error": str(fe)}
    
    except Exception as e:
        return {"error": str(e)}

def handler(event, context):

    body = json.loads(event['body'])
    email = body.get('email')
    password = body.get('password')

    if not email or not password:
        return {
            'statusCode': 404,
            'body': json.dumps({"message": "Email and passwors are required"})
        }
    response = register_user(email, password, secretName)
    logger.info(f'Response from create user call: {response}')

    if 'user_id' in response:
        # store user to table
        add_user(response['user_id'], email)
        return {
                'statusCode': 200,
                'body': json.dumps({"message": "User created successfully", "user_id": response["user_id"]})
            }
    else:
        if 'error' in response and 'already exists' in response['error'].lower():
            return {
                'statusCode': 409,
                'body': json.dumps({'message': 'User already exists'})
            }
        return {
            'statusCode': 500,
            'body': json.dumps({'message': response.get('error', 'Unknown error occured')})
        }

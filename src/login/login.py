import json
import requests
import logging
import os
import secretmanager

logger = logging.getLogger()
logger.setLevel(logging.INFO)
secretName = os.environ.get('SECRET_NAME')
secretJson = secretmanager.get_secret(secretName)
apiKey = secretJson['apiKey']


def authenticate_user(email, password):
    url = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={apiKey}"
    header = {"Content-Type": "application/json"}
    data = {
        "email": email,
        "password": password,
        "returnSecureToken": True
    }
    response = requests.post(url, headers=header, json=data)
    return response.json()

def handler(event, context):
    body = json.loads(event["body"])
    email = body.get('email')
    password = body.get('password')

    if not email or not password:
        return {'statusCode': 400, 'body': json.dumps({'message': 'Email and password are required'})}
    
    try:
        auth_response = authenticate_user(email, password)
        logger.info(f'Auth Response: {auth_response}')
        if 'idToken' in auth_response and 'refreshToken' in auth_response:
            return {'statusCode': 200, 'body': json.dumps({'idToken': auth_response['idToken'], 'refreshToken': auth_response['refreshToken'], 'expiresIn': auth_response['expiresIn'] })}
        else:
            return {'statusCode': 401, 'body': json.dumps({'message': 'Authentication failed'})}
    except Exception as e:
        logger.error(f'Error during authtication: {e}')
        return {'statusCode': 500, 'body': json.dumps({'message': 'Unknown error occured'})}
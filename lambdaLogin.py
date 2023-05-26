import json
import uuid
import hashlib
import boto3

# AWS Integration
dynamodb = boto3.client('dynamodb')
table = dynamodb.Table('wtf_login')

def lambda_handler(event, context):
    if event['httpMethod'] == 'GET':
        return index()
    elif event['httpMethod'] == 'POST':
        if event['path'] == '/login':
            return login(event['body'])
        elif event['path'] == '/register':
            return register(event['body'])
        else:
            return {
                'statusCode': 404,
                'body': 'Not Found'
            }

def index():
    return {
        'statusCode': 200,
        'body': '<html><body>Login Page</body></html>'
    }

def login(body):
    data = json.loads(body)
    username = data['userName']
    password = hashlib.sha512(data['password'].encode('utf-8')).hexdigest()

    response = table.get_item(Key={'name': username})
    user = response.get('Item')

    if user and user['password'] == password:
        return {
            'statusCode': 200,
            'body': str(uuid.uuid4())
        }
    else:
        return {
            'statusCode': 400,
            'body': 'Who are you?'
        }

def register(body):
    data = json.loads(body)
    password = data['password']
    vpassword = data['verifyPassword']

    # Compare the password with the verify password to determine whether to push the user
    if password == vpassword:
        password = hashlib.sha512(password.encode('utf-8')).hexdigest()

        user = {
            'name': data['userName'],
            'email': data['email'],
            'password': data['password'],
        }

        password = ''
        vpassword = ''

        try:
            table.put_item(Item=user)
            print(data['userName'] + " made an account.")
            return {
                'statusCode': 200,
                'body': 'Account created, please log in.'
            }
        except Exception as e:
            return {
                'statusCode': 400,
                'body': str(e)
            }
    else:
        return {
            'statusCode': 400,
            'body': 'Passwords do not match'
        }
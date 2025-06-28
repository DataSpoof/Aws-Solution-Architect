import json
import boto3
from decimal import Decimal

def lambda_handler(event, context):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('employee')
    
    operation = event.get('operation')
    
    if operation == 'create':
        return create_item(table, event)
    elif operation == 'read':
        return read_item(table, event)
    elif operation == 'update':
        return update_item(table, event)
    elif operation == 'delete':
        return delete_item(table, event)
    else:
        return {
            'statusCode': 400,
            'body': json.dumps('Invalid operation')
        }

def create_item(table, event):
    item = {
        'id': int(event['id']),  # Convert id to integer
        'name': event['name'],
        'age': event['age']
    }
    
    table.put_item(Item=item)
    
    return {
        'statusCode': 200,
        'body': json.dumps('Item created successfully!')
    }

def read_item(table, event):
    response = table.get_item(
        Key={
            'id': int(event['id'])  # Convert id to integer
        }
    )
    
    item = response.get('Item', None)
    
    return {
        'statusCode': 200,
        'body': json.dumps(item, cls=DecimalEncoder)
    }

def update_item(table, event):
    response = table.update_item(
        Key={
            'id': int(event['id'])  # Convert id to integer
        },
        UpdateExpression="set #name = :name, age = :age",
        ExpressionAttributeValues={
            ':name': event['name'],
            ':age': event['age']
        },
        ExpressionAttributeNames={
            "#name": "name"
        },
        ReturnValues="UPDATED_NEW"
    )
    
    return {
        'statusCode': 200,
        'body': json.dumps('Item updated successfully!')
    }

def delete_item(table, event):
    table.delete_item(
        Key={
            'id': int(event['id'])  # Convert id to integer
        }
    )
    
    return {
        'statusCode': 200,
        'body': json.dumps('Item deleted successfully!')
    }

class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return float(obj)
        return super(DecimalEncoder, self).default(obj)

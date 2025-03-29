import boto3
from botocore.exceptions import ClientError
import os

class DynamoDBService:
    def __init__(self):
        self.dynamodb = boto3.resource('dynamodb')
        self.table = self.dynamodb.Table(os.getenv('DYNAMODB_TABLE_NAME', 'gradpict-memories'))
    
    def create_memory(self, memory_data):
        try:
            response = self.table.put_item(
                Item=memory_data
            )
            return response
        except ClientError as e:
            print(f"Error creating memory: {e}")
            raise
    
    def get_memory(self, memory_id, user_id):
        try:
            response = self.table.get_item(
                Key={
                    'id': memory_id,
                    'user_id': user_id
                }
            )
            return response.get('Item')
        except ClientError as e:
            print(f"Error getting memory: {e}")
            raise
    
    def update_memory(self, memory_id, user_id, update_data):
        try:
            update_expression = "SET "
            expression_attribute_names = {}
            expression_attribute_values = {}
            
            for key, value in update_data.items():
                update_expression += f"#{key} = :{key}, "
                expression_attribute_names[f"#{key}"] = key
                expression_attribute_values[f":{key}"] = value
            
            update_expression = update_expression.rstrip(", ")
            
            response = self.table.update_item(
                Key={
                    'id': memory_id,
                    'user_id': user_id
                },
                UpdateExpression=update_expression,
                ExpressionAttributeNames=expression_attribute_names,
                ExpressionAttributeValues=expression_attribute_values,
                ReturnValues="ALL_NEW"
            )
            return response.get('Attributes')
        except ClientError as e:
            print(f"Error updating memory: {e}")
            raise

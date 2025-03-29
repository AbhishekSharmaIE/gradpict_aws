import boto3
import os
from botocore.exceptions import ClientError

def create_s3_bucket():
    s3 = boto3.client('s3')
    bucket_name = os.getenv('AWS_STORAGE_BUCKET_NAME')
    region = os.getenv('AWS_S3_REGION_NAME', 'eu-west-2')
    
    try:
        s3.create_bucket(
            Bucket=bucket_name,
            CreateBucketConfiguration={'LocationConstraint': region}
        )
        print(f"Created S3 bucket: {bucket_name}")
        
        # Enable versioning
        s3.put_bucket_versioning(
            Bucket=bucket_name,
            VersioningConfiguration={'Status': 'Enabled'}
        )
        
        # Configure CORS
        cors_configuration = {
            'CORSRules': [{
                'AllowedHeaders': ['*'],
                'AllowedMethods': ['GET', 'PUT', 'POST', 'DELETE'],
                'AllowedOrigins': ['*'],
                'ExposeHeaders': ['ETag']
            }]
        }
        s3.put_bucket_cors(
            Bucket=bucket_name,
            CORSConfiguration=cors_configuration
        )
        
        return bucket_name
    except ClientError as e:
        print(f"Error creating S3 bucket: {e}")
        raise

def create_dynamodb_table():
    dynamodb = boto3.resource('dynamodb')
    table_name = os.getenv('DYNAMODB_TABLE_NAME', 'gradpict-memories')
    
    try:
        table = dynamodb.create_table(
            TableName=table_name,
            KeySchema=[
                {'AttributeName': 'id', 'KeyType': 'HASH'},
                {'AttributeName': 'user_id', 'KeyType': 'RANGE'}
            ],
            AttributeDefinitions=[
                {'AttributeName': 'id', 'AttributeType': 'S'},
                {'AttributeName': 'user_id', 'AttributeType': 'S'}
            ],
            ProvisionedThroughput={
                'ReadCapacityUnits': 5,
                'WriteCapacityUnits': 5
            }
        )
        print(f"Created DynamoDB table: {table_name}")
        return table
    except ClientError as e:
        if e.response['Error']['Code'] == 'ResourceInUseException':
            print(f"Table {table_name} already exists")
            return dynamodb.Table(table_name)
        else:
            raise

def create_sns_topic():
    sns = boto3.client('sns')
    topic_name = 'gradpict-notifications'
    
    try:
        response = sns.create_topic(Name=topic_name)
        print(f"Created SNS topic: {topic_name}")
        print(f"Topic ARN: {response['TopicArn']}")
        return response['TopicArn']
    except ClientError as e:
        print(f"Error creating SNS topic: {e}")
        raise

def setup_aws_resources():
    try:
        # Create S3 bucket
        bucket_name = create_s3_bucket()
        
        # Create DynamoDB table
        create_dynamodb_table()
        
        # Create SNS topic
        topic_arn = create_sns_topic()
        
        print("\nAWS Resources Setup Complete!")
        print(f"S3 Bucket: {bucket_name}")
        print(f"DynamoDB Table: {os.getenv('DYNAMODB_TABLE_NAME')}")
        print(f"SNS Topic ARN: {topic_arn}")
        
    except Exception as e:
        print(f"Error during AWS setup: {e}")
        raise

if __name__ == "__main__":
    setup_aws_resources()

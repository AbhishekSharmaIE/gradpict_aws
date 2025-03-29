import boto3
from botocore.exceptions import ClientError
import os

class S3Service:
    def __init__(self):
        self.s3 = boto3.client('s3')
        self.bucket_name = os.getenv('AWS_STORAGE_BUCKET_NAME')
    
    def upload_file(self, file_obj, file_name, content_type=None):
        try:
            extra_args = {'ContentType': content_type} if content_type else {}
            self.s3.upload_fileobj(
                file_obj,
                self.bucket_name,
                file_name,
                ExtraArgs=extra_args
            )
            return f"https://{self.bucket_name}.s3.amazonaws.com/{file_name}"
        except ClientError as e:
            print(f"Error uploading file to S3: {e}")
            raise
    
    def delete_file(self, file_name):
        try:
            self.s3.delete_object(
                Bucket=self.bucket_name,
                Key=file_name
            )
            return True
        except ClientError as e:
            print(f"Error deleting file from S3: {e}")
            raise

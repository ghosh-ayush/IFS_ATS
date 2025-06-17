import boto3
from src.config import AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, S3_BUCKET

s3 = boto3.client(
    's3',
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY
)

def upload_fileobj(fileobj, key):
    """Upload a file-like object to S3."""
    s3.upload_fileobj(fileobj, S3_BUCKET, key)


def download_file(key, dest_path):
    """Download an S3 object to a local path."""
    s3.download_file(S3_BUCKET, key, dest_path)

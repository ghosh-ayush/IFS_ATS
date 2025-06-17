import boto3
from src.config import (
    AWS_ACCESS_KEY_ID,
    AWS_SECRET_ACCESS_KEY,
    S3_BUCKET,
    S3_INDEX_BUCKET,
)

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


def upload_index(path: str, key: str) -> None:
    """Upload a FAISS index file to the index bucket."""
    s3.upload_file(path, S3_INDEX_BUCKET, key)


def download_index(key: str, dest_path: str) -> None:
    """Download a FAISS index from the index bucket."""
    s3.download_file(S3_INDEX_BUCKET, key, dest_path)

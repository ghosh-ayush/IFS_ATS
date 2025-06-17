from fastapi import FastAPI, UploadFile
import boto3

from ..config import (
    AWS_ACCESS_KEY_ID,
    AWS_SECRET_ACCESS_KEY,
    RDS_HOST,
    RDS_USER,
    RDS_PASS,
    RDS_DB,
    OPENAI_API_KEY,
)

app = FastAPI(title="IFS ATS")

s3 = boto3.client(
    "s3",
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
)

BUCKET = "ifs-resumes"

@app.post("/upload-resume/")
async def upload_resume(user_id: str, file: UploadFile):
    key = f"{user_id}/{file.filename}"
    s3.upload_fileobj(file.file, BUCKET, key)
    return {"message": "uploaded", "s3_key": key}

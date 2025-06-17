import logging
from fastapi import FastAPI, UploadFile, Depends
from sqlalchemy.orm import Session
import boto3
from mangum import Mangum

from src.api.auth import get_current_user

from src.utils.s3_helper import upload_fileobj
from src.db.models import Base, Resume, JobProfile
from src.db.database import SessionLocal, engine
from src.rag.vector_store import build_store
from src.rag.generation import make_chain

logging.basicConfig(level=logging.INFO)
app = FastAPI()

cloudwatch = boto3.client("cloudwatch")

def log_metric(name: str) -> None:
    """Send a custom metric to CloudWatch."""
    cloudwatch.put_metric_data(
        Namespace="IFSATS",
        MetricData=[{"MetricName": name, "Value": 1, "Unit": "Count"}],
    )

Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/upload-resume/")
async def upload_resume(
    user_id: int,
    file: UploadFile,
    db: Session = Depends(get_db),
    _: int = Depends(get_current_user),
):
    log_metric("upload_resume")
    key = f"{user_id}/{file.filename}"
    upload_fileobj(file.file, key)
    db.add(Resume(user_id=user_id, s3_key=key))
    db.commit()
    logging.info("uploaded %s for user %s", key, user_id)
    return {"message": "Uploaded", "s3_key": key}


@app.get("/job-profiles/")
def list_job_profiles(db: Session = Depends(get_db), _: int = Depends(get_current_user)):
    log_metric("job_profiles")
    return db.query(JobProfile).all()


@app.post("/generate/")
def generate_application(
    user_id: int,
    job_description: str,
    db: Session = Depends(get_db),
    _: int = Depends(get_current_user),
):
    log_metric("generate")
    resumes = db.query(Resume).filter_by(user_id=user_id).all()
    keys = [r.s3_key for r in resumes]
    index_key = f"{user_id}/faiss.index"
    store = build_store(keys, index_key=index_key)
    chain = make_chain(store)
    logging.info("generated application for user %s", user_id)
    return chain.run(job_description)

handler = Mangum(app)

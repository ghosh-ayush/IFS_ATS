import logging
from fastapi import FastAPI, UploadFile, Depends
from sqlalchemy.orm import Session
from prometheus_client import Counter, generate_latest

from src.api.auth import get_current_user

from src.utils.s3_helper import upload_fileobj
from src.db.models import Base, Resume, JobProfile
from src.db.database import SessionLocal, engine
from src.rag.vector_store import build_store
from src.rag.generation import make_chain

logging.basicConfig(level=logging.INFO)
app = FastAPI()

REQUEST_COUNT = Counter("requests_total", "Total HTTP requests", ["endpoint"])

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
    REQUEST_COUNT.labels(endpoint="upload_resume").inc()
    key = f"{user_id}/{file.filename}"
    upload_fileobj(file.file, key)
    db.add(Resume(user_id=user_id, s3_key=key))
    db.commit()
    logging.info("uploaded %s for user %s", key, user_id)
    return {"message": "Uploaded", "s3_key": key}


@app.get("/job-profiles/")
def list_job_profiles(db: Session = Depends(get_db), _: int = Depends(get_current_user)):
    REQUEST_COUNT.labels(endpoint="job_profiles").inc()
    return db.query(JobProfile).all()


@app.post("/generate/")
def generate_application(
    user_id: int,
    job_description: str,
    db: Session = Depends(get_db),
    _: int = Depends(get_current_user),
):
    REQUEST_COUNT.labels(endpoint="generate").inc()
    resumes = db.query(Resume).filter_by(user_id=user_id).all()
    keys = [r.s3_key for r in resumes]
    index_key = f"{user_id}/faiss.index"
    store = build_store(keys, index_key=index_key)
    chain = make_chain(store)
    logging.info("generated application for user %s", user_id)
    return chain.run(job_description)


@app.get("/metrics")
def metrics():
    return generate_latest(), 200, {"Content-Type": "text/plain"}

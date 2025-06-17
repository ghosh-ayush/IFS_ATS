from fastapi import FastAPI, UploadFile, Depends
from sqlalchemy.orm import Session

from src.utils.s3_helper import upload_fileobj
from src.db.models import Base, Resume, JobProfile
from src.db.database import SessionLocal, engine
from src.rag.vector_store import build_store
from src.rag.generation import make_chain

app = FastAPI()

Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/upload-resume/")
async def upload_resume(user_id: int, file: UploadFile, db: Session = Depends(get_db)):
    key = f"{user_id}/{file.filename}"
    upload_fileobj(file.file, key)
    db.add(Resume(user_id=user_id, s3_key=key))
    db.commit()
    return {"message": "Uploaded", "s3_key": key}


@app.get("/job-profiles/")
def list_job_profiles(db: Session = Depends(get_db)):
    return db.query(JobProfile).all()


@app.post("/generate/")
def generate_application(job_description: str):
    store = build_store(["input/example_user/resume_1.txt"])
    chain = make_chain(store)
    return chain.run(job_description)
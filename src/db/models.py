from sqlalchemy import Column, Integer, String, Text, TIMESTAMP, ForeignKey, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    email = Column(String(255), unique=True, nullable=False)
    password_hash = Column(Text, nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.now())

class Resume(Base):
    __tablename__ = 'resumes'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    s3_key = Column(String(255), nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.now())

class JobProfile(Base):
    __tablename__ = 'job_profiles'
    id = Column(Integer, primary_key=True)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    skills = Column(JSON, nullable=False)
    experience_level = Column(String(100))

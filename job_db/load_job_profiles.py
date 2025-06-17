"""Bulk load job profiles into PostgreSQL."""

import json
from sqlalchemy import create_engine, Table, Column, Integer, String, Text, MetaData, insert
from sqlalchemy.dialects.postgresql import ARRAY
from src.config import DB_URL

engine = create_engine(DB_URL)
metadata = MetaData()

job_profiles = Table(
    'job_profiles', metadata,
    Column('id', Integer, primary_key=True),
    Column('title', String(255)),
    Column('description', Text),
    Column('skills', ARRAY(String)),
    Column('experience_level', String(100))
)

def load():
    """Read job_profiles.json and insert records."""
    with open('job_db/job_profiles.json') as f:
        data = json.load(f)
    with engine.connect() as conn:
        for jp in data:
            stmt = insert(job_profiles).values(
                title=jp['title'],
                description=jp['description'],
                skills=jp['skills'],
                experience_level=jp.get('experience_level')
            )
            conn.execute(stmt)

if __name__ == '__main__':
    load()

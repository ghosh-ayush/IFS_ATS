"""Central configuration loader using python-decouple."""

from decouple import config

AWS_ACCESS_KEY_ID = config("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = config("AWS_SECRET_ACCESS_KEY")
RDS_HOST = config("RDS_HOST")
RDS_USER = config("RDS_USER")
RDS_PASS = config("RDS_PASS")
RDS_DB = config("RDS_DB")
OPENAI_API_KEY = config("OPENAI_API_KEY")

DB_URL = f"postgresql://{RDS_USER}:{RDS_PASS}@{RDS_HOST}/{RDS_DB}"
S3_BUCKET = "ifs-resumes"

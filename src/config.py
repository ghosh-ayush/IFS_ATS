"""Central configuration loader using python-decouple."""
import os
from decouple import config

import json
import boto3


def _load_secrets():
    """Fetch secrets from AWS Secrets Manager if SECRETS_NAME is set."""
    name = config("SECRETS_NAME", default=None)
    if not name:
        return {}
    client = boto3.client("secretsmanager")
    try:
        resp = client.get_secret_value(SecretId=name)
    except Exception:
        return {}
    return json.loads(resp.get("SecretString", "{}"))


_secrets = _load_secrets()

AWS_ACCESS_KEY_ID = config("AWS_ACCESS_KEY_ID", default=_secrets.get("AWS_ACCESS_KEY_ID"))
AWS_SECRET_ACCESS_KEY = config("AWS_SECRET_ACCESS_KEY", default=_secrets.get("AWS_SECRET_ACCESS_KEY"))
RDS_HOST = config("RDS_HOST", default=_secrets.get("RDS_HOST"))
RDS_USER = config("RDS_USER", default=_secrets.get("RDS_USER"))
RDS_PASS = config("RDS_PASS", default=_secrets.get("RDS_PASS"))
RDS_DB = config("RDS_DB", default=_secrets.get("RDS_DB"))
OPENAI_API_KEY = config("OPENAI_API_KEY", default=_secrets.get("OPENAI_API_KEY"))

if None in (RDS_HOST, RDS_USER, RDS_PASS, RDS_DB):
    DB_URL = "sqlite:///./test.db"
else:
    DB_URL = f"postgresql://{RDS_USER}:{RDS_PASS}@{RDS_HOST}/{RDS_DB}"
S3_BUCKET = "ifs-resumes"
S3_INDEX_BUCKET = "ifs-resumes-index"

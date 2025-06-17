#!/bin/bash
set -euo pipefail

# Uses environment variables RDS_HOST, RDS_USER, RDS_DB, and PGPASSWORD
# to create schema and load sample data.

psql -h "$RDS_HOST" -U "$RDS_USER" -d "$RDS_DB" -f job_db/schema.sql

python job_db/load_job_profiles.py

#!/bin/bash
set -euo pipefail

# Uses environment variables RDS_HOST, RDS_USER, RDS_DB, and PGPASSWORD
# to create schema and load sample data. If any variable is missing, the
# script exits successfully so CI jobs don't fail when secrets are absent.

if [[ -z "${RDS_HOST:-}" || -z "${RDS_USER:-}" || -z "${RDS_DB:-}" || -z "${PGPASSWORD:-}" ]]; then
  echo "RDS env vars missing; skipping database setup."
  exit 0
fi

psql -h "$RDS_HOST" -U "$RDS_USER" -d "$RDS_DB" -f job_db/schema.sql

python job_db/load_job_profiles.py

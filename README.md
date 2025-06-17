# IFS ATS

A skeleton project for an ATS-friendly resume generator using Langchain and AWS.

## Repository Layout

- `input/` – raw resumes and profile links (mirrored in S3)
- `job_db/` – SQL schemas or scripts for job profile data
- `src/` – backend code
  - `api/` – FastAPI endpoints deployable via AWS Lambda and API Gateway
  - `rag/` – Langchain retrieval and generation utilities
  - `db/` – ORM models and migrations
  - `utils/` – helpers for S3, RDS, and scraping
- `frontend/` – static site served via Amazon S3/CloudFront
- `scripts/` – automation and scraping scripts
- `.env.example` – list of environment variables

## Getting Started

1. Copy `.env.example` to `.env` and fill in your AWS and OpenAI credentials.
   Configuration variables are loaded with `python-decouple` from this file.
The `scripts/setup_db.sh` script used in CI checks for required RDS environment
variables and simply skips setup if they are missing. This allows the workflow
to succeed even when database credentials aren't provided.

   
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the FastAPI app locally:
   ```bash
   uvicorn src.api.main:app --reload
   ```
   The same application can be deployed to AWS Lambda using the `handler` exposed in `src.api.main`.
4. Initialize the database schema with Alembic:
   ```bash
   alembic upgrade head
   ```
To load example job profiles into your database, run:
```bash
python job_db/load_job_profiles.py
```

This project stores resumes in S3, metadata in RDS, and uses Langchain with Retrieval-Augmented Generation to craft job-specific resumes and cover letters.

The `src/rag` package contains helpers for Langchain's retrieval-augmented generation. `vector_store.build_store()` now leverages Amazon OpenSearch Service when `OPENSEARCH_ENDPOINT` is configured, falling back to a local FAISS index otherwise. Use `generation.make_chain()` to create the RetrievalQA chain.

All API endpoints emit custom metrics to Amazon CloudWatch instead of Prometheus.

## Development

Run lint and tests locally with:
```bash
flake8
pytest -q
```

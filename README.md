# IFS ATS

A skeleton project for an ATS-friendly resume generator using Langchain and AWS.

## Repository Layout

- `input/` – raw resumes and profile links (mirrored in S3)
- `job_db/` – SQL schemas or scripts for job profile data
- `src/` – backend code
  - `api/` – FastAPI endpoints
  - `rag/` – Langchain retrieval and generation utilities
  - `db/` – ORM models and migrations
  - `utils/` – helpers for S3, RDS, and scraping
- `frontend/` – static site served via GitHub Pages
- `scripts/` – automation and scraping scripts
- `.env.example` – list of environment variables

## Getting Started

1. Copy `.env.example` to `.env` and fill in your AWS and OpenAI credentials.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the FastAPI app:
   ```bash
   uvicorn src.api.main:app --reload
   ```

This project stores resumes in S3, metadata in RDS, and uses Langchain with Retrieval-Augmented Generation to craft job-specific resumes and cover letters.

"""Simple job scraper placeholder with scheduling support."""

import json
import schedule
import time


def scrape_and_save():
    """Placeholder scraping logic."""
    # TODO: replace with real scraping
    sample = {
        "title": "Example",
        "description": "Sample desc",
        "skills": ["python"],
        "experience_level": "junior",
    }
    with open("job_db/job_profiles.json", "w") as fh:
        json.dump([sample], fh)


def main():
    schedule.every().day.at("02:00").do(scrape_and_save)
    while True:
        schedule.run_pending()
        time.sleep(60)


if __name__ == "__main__":
    main()

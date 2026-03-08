# scraper/scrape_jobs.py
import requests
from bs4 import BeautifulSoup
import argparse
import logging
import json
from datetime import datetime
import time

# -----------------------------
# Logger Setup
# -----------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# -----------------------------
# Scraper Class
# -----------------------------
class JobScraper:

    BASE_URL = "https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search"

    def __init__(self, role, location, pages):
        self.role = role
        self.location = location
        self.pages = pages
        self.jobs = []

    def scrape(self):

        headers = {
            "User-Agent": "Mozilla/5.0"
        }

        for page in range(self.pages):

            params = {
                "keywords": self.role,
                "location": self.location,
                "start": page * 25
            }

            logging.info(f"Scraping page {page+1}")

            response = requests.get(self.BASE_URL, params=params, headers=headers)

            if response.status_code != 200:
                logging.warning("Failed request")
                continue

            soup = BeautifulSoup(response.text, "html.parser")

            job_cards = soup.find_all("li")

            for job in job_cards:

                title = job.find("h3", class_="base-search-card__title")
                company = job.find("h4", class_="base-search-card__subtitle")
                location = job.find("span", class_="job-search-card__location")
                link = job.find("a", class_="base-card__full-link")

                record = {
                    "job_id": link["href"].split("/")[-1] if link else None,
                    "title": title.text.strip() if title else None,
                    "company": company.text.strip() if company else None,
                    "location": location.text.strip() if location else None,
                    "job_link": link["href"] if link else None,
                    "scraped_at": datetime.utcnow().isoformat()
                }

                self.jobs.append(record)

            time.sleep(1)

        logging.info(f"Total jobs scraped: {len(self.jobs)}")

        return self.jobs


# -----------------------------
# Save Data
# -----------------------------
def save_json(data, output):

    with open(output, "w") as f:
        json.dump(data, f, indent=2)

    logging.info(f"Saved data to {output}")


# -----------------------------
# CLI Entry
# -----------------------------
def main():

    parser = argparse.ArgumentParser()

    parser.add_argument("--role", default="data engineer")
    parser.add_argument("--location", default="India")
    parser.add_argument("--pages", type=int, default=3)
    parser.add_argument("--output", default="jobs_raw.json")

    args = parser.parse_args()

    scraper = JobScraper(
        role=args.role,
        location=args.location,
        pages=args.pages
    )

    jobs = scraper.scrape()

    save_json(jobs, args.output)


if __name__ == "__main__":
    main()

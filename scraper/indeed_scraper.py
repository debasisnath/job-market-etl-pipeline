import requests
from bs4 import BeautifulSoup
from datetime import datetime
import time
import re
from scraper.base_scraper import BaseScraper
from utils.logger import get_logger

logger = get_logger(__name__)


class IndeedScraper(BaseScraper):

    BASE_URL = "https://www.indeed.com/api/jobs"

    headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
            "Accept-Language": "en-US,en;q=0.9",
    }

    SKILL_KEYWORDS = [
        "spark",
        "pyspark",
        "hadoop",
        "kafka",
        "airflow",
        "snowflake",
        "databricks",
        "aws",
        "azure",
        "gcp",
        "sql",
        "python",
        "scala",
        "delta lake",
    ]

    def scrape(self):

        

        for page in range(self.pages):

            params = {
                "q": self.role,
                "l": self.location,
                "start": page * 10
            }

            logger.info(f"Scraping Indeed page {page+1}")

            response = requests.get(self.BASE_URL, params=params, headers=self.headers)

            logger.info(f"Response text (first 500 chars): {response.text[:500]}")

            if response.status_code != 200:
                logger.warning("Request failed")
                continue

            soup = BeautifulSoup(response.text, "html.parser")

            job_cards = soup.select("a.tapItem")

            logger.info(f"Found {len(job_cards)} job cards")

            for job in job_cards:

                title = job.select_one("h2.jobTitle")
                company = job.select_one("span.companyName")
                location = job.select_one("div.companyLocation")

                link = job.get("href")


                record = {
                    "job_id": str(hash(title.text if title else "")),
                    "title": title.text.strip() if title else None,
                    "company": company.text.strip() if company else None,
                    "location": location.text.strip() if location else None,
                    "job_link": f"https://in.indeed.com{link}" if link else None,
                    "source": "indeed",
                    "scraped_at": datetime.utcnow().isoformat()
                }

                self.jobs.append(record)

            time.sleep(1)

        logger.info(f"Total Indeed jobs scraped: {len(self.jobs)}")

        return self.jobs
    

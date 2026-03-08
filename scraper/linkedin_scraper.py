import requests
from bs4 import BeautifulSoup
from datetime import datetime, timezone
import time

from scraper.base_scraper import BaseScraper
from models.job_model import Job


class LinkedInScraper(BaseScraper):

    BASE_URL = "https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search"

    def scrape(self):

        headers = {"User-Agent": "Mozilla/5.0"}

        for page in range(self.pages):

            params = {
                "keywords": self.role,
                "location": self.location,
                "start": page * 25
            }

            response = requests.get(self.BASE_URL, params=params, headers=headers)

            soup = BeautifulSoup(response.text, "html.parser")

            job_cards = soup.find_all("li")

            for job in job_cards:

                title = job.find("h3")
                company = job.find("h4")
                location = job.find("span", class_="job-search-card__location")
                link = job.find("a", class_="base-card__full-link")

                job_obj = Job(
                    job_id=link["href"] if link else None,
                    title=title.text.strip() if title else None,
                    company=company.text.strip() if company else None,
                    location=location.text.strip() if location else None,
                    job_link=link["href"] if link else None,
                    source="linkedin",
                    scraped_at=datetime.now(timezone.utc).isoformat()
                )

                self.jobs.append(job_obj.__dict__)

            time.sleep(1)

        return self.jobs



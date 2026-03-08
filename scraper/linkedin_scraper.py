import re

import requests
from bs4 import BeautifulSoup
from datetime import datetime, timezone
import time

from scraper.base_scraper import BaseScraper
from models.job_model import Job

from utils.logger import get_logger

logger = get_logger(__name__)

class LinkedInScraper(BaseScraper):

    BASE_URL = "https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search"

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

    headers = {"User-Agent": "Mozilla/5.0"}

    def scrape(self):

        

        logger.info(f"Starting LinkedIn scrape for {self.role}")

        for page in range(self.pages):

            params = {
                "keywords": self.role,
                "location": self.location,
                "start": page * 25
            }

            response = requests.get(self.BASE_URL, params=params, headers=self.headers)

            soup = BeautifulSoup(response.text, "html.parser")

            job_cards = soup.find_all("li")

            logger.info("Scraping page %s", page+1)

            for job in job_cards:

                title = job.find("h3")
                company = job.find("h4")
                location = job.find("span", class_="job-search-card__location")
                link = job.find("a", class_="base-card__full-link")

                job_id_numeric = self.extract_job_id(link["href"])
                description = self.fetch_linkedin_description(job_id_numeric)
                skills = self.extract_skills(description)

                job_obj = Job(
                    job_id=link["href"] if link else None,
                    title=title.text.strip() if title else None,
                    company=company.text.strip() if company else None,
                    location=location.text.strip() if location else None,
                    job_link=link["href"] if link else None,
                    source="linkedin",
                    skills=skills,
                    scraped_at=datetime.now(timezone.utc).isoformat()
                )

                self.jobs.append(job_obj.__dict__)

            time.sleep(1)
            logger.info("Finished scraping page %s", page+1)

        logger.info(f"Total jobs scraped: {len(self.jobs)}")
        return self.jobs


    def extract_job_id(self,job_url):
        match = re.search(r'-(\d+)', job_url)
        if match:
            return match.group(1)
        return None
    
    def fetch_linkedin_description(self, job_id):

        url = self.BASE_URL + job_id
        response = requests.get(url, headers=self.headers)
        soup = BeautifulSoup(response.text, "html.parser")
        desc = soup.find("div", class_="show-more-less-html__markup")

        if desc:
            return desc.text.strip()

        return None

    def extract_skills(self, text):

        if not text:
            return []

        text = text.lower()

        skills = []

        for skill in self.SKILL_KEYWORDS:
            if skill in text:
                skills.append(skill)

        return list(set(skills))


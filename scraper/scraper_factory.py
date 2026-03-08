from scraper.linkedin_scraper import LinkedInScraper
from scraper.indeed_scraper import IndeedScraper


def get_scraper(source, role, location, pages):

    if source == "linkedin":
        return LinkedInScraper(role, location, pages)

    if source == "indeed":
        return IndeedScraper(role, location, pages)

    raise ValueError(f"Unsupported source: {source}")


# GlassdoorScraper
# NaukriScraper



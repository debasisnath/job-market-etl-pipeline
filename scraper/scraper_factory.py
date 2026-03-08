from scraper.linkedin_scraper import LinkedInScraper

def get_scraper(source, role, location, pages):

    if source == "linkedin":
        return LinkedInScraper(role, location, pages)

    raise ValueError(f"Unsupported source: {source}")

# IndeedScraper
# GlassdoorScraper
# NaukriScraper



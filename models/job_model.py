from dataclasses import dataclass

@dataclass
class Job:

    job_id: str
    title: str
    company: str
    location: str
    job_link: str
    source: str
    scraped_at: str

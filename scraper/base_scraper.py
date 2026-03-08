from abc import ABC, abstractmethod

class BaseScraper(ABC):

    def __init__(self, role, location, pages):
        self.role = role
        self.location = location
        self.pages = pages
        self.jobs = []

    @abstractmethod
    def scrape(self):
        pass



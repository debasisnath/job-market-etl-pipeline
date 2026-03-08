import argparse

from scraper.scraper_factory import get_scraper
from utils.file_writer import save_json


def main():

    parser = argparse.ArgumentParser()

    parser.add_argument("--source", default="linkedin")
    parser.add_argument("--role", default="data engineer")
    parser.add_argument("--location", default="India")
    parser.add_argument("--pages", type=int, default=3)
    parser.add_argument("--output", default="jobs_raw.json")

    args = parser.parse_args()

    scraper = get_scraper(
        args.source,
        args.role,
        args.location,
        args.pages
    )

    jobs = scraper.scrape()

    save_json(jobs, args.output)


if __name__ == "__main__":
    main()




##### Folder structure create

```python

# structure_create.py
import os
from pathlib import Path

# Define the project structure
structure = {
    "scraper": ["scrape_jobs.py"],
    "data_pipeline": ["pyspark_etl.py", "transform_jobs.py", "data_quality_checks.py"],
    "configs": ["spark_config.yaml"],
    "notebooks": ["analysis_dashboard.ipynb"],
    "infra": ["s3_setup.tf"],
    "data_sample": ["sample_jobs.json"],
    ".": [ "architecture.png"]  # root-level files
}

def create_structure(base_dir="job-market-etl-pipeline"):
    base_path = Path(base_dir)
    base_path.mkdir(parents=True, exist_ok=True)

    for folder, files in structure.items():
        folder_path = base_path / folder if folder != "." else base_path
        folder_path.mkdir(parents=True, exist_ok=True)

        for file in files:
            file_path = folder_path / file
            if not file_path.exists():
                file_path.touch()
                print(f"Created: {file_path}")

if __name__ == "__main__":
    create_structure()

```

##### quick push 
```bash 
git add . && git commit -m "update: $(date '+%Y-%m-%d %H:%M:%S') | $(date +%s)" && git push origin main

```

##### RUN_SCRAPER
```bash
python -m pipeline.run_scraper \
    --source linkedin \
    --role "data engineer" \
    --location India \
    --pages 5 \
    --output data_sample/jobs_raw.json

```





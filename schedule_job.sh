rm -f jobs.json
scrapy crawl job_update_bot -o jobs.json
python app.py
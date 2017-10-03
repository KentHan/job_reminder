import json
from dao import JobDAO
from job_update_bot.spiders.items import JobItem

dao = JobDAO()

def diff(first, second):
    second = set(second)
    return [item for item in first if item not in second]

def compare():
	
	recorded_job_items = dao.query_all_jobs()
	recorded_job_title_list = [job_item['job_title'] for job_item in recorded_job_items]

	json_data=open("jobs.json").read()
	latest_job_items = json.loads(json_data)
	latest_job_title_list = [job_item['job_title'] for job_item in latest_job_items]
	print(latest_job_title_list)

	added_jobs = diff(latest_job_title_list, recorded_job_title_list)
	notify_added_jobs(added_jobs)
	update_added_jobs_in_db(added_jobs)

	removed_jobs = diff(recorded_job_title_list, latest_job_title_list)
	notify_removed_jobs(removed_jobs)
	update_removed_jobs_in_db(removed_jobs)

def notify_added_jobs(added_jobs):
	print('added jobs: ' + str(added_jobs))

def update_added_jobs_in_db(added_jobs):
	for job_title in added_jobs:
		job = JobItem({'job_title': job_title})
		dao.add_job(job)

def notify_removed_jobs(removed_jobs):
	print('removed jobs: ' + str(removed_jobs))

def update_removed_jobs_in_db(removed_jobs):
	for job_title in removed_jobs:
		job = JobItem({'job_title': job_title})
		dao.delete_job(job)


# job = JobItem()
# job['job_title'] = "RD"
# print(job)
compare()
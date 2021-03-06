# -*- coding: utf-8 -*-

import json, os
from dao import JobDAO
from job_update_bot.spiders.items import JobItem
from message import MessageApi

dao = JobDAO()
message_api = MessageApi()
target = os.getenv("TARGET")

def diff(first, second):
    second = set(second)
    first = set(first)
    return [item for item in first if item not in second]

def compare():
    recorded_job_items = dao.query_all_jobs()
    recorded_job_title_list = [job_item['job_title'] for job_item in recorded_job_items]

    json_data=open("jobs.json").read()
    global latest_job_items
    latest_job_items = json.loads(json_data)
    latest_job_title_list = [job_item['job_title'] for job_item in latest_job_items]
    print(latest_job_title_list)

    added_jobs = diff(latest_job_title_list, recorded_job_title_list)
    removed_jobs = diff(recorded_job_title_list, latest_job_title_list)

    if len(added_jobs + removed_jobs) == 0:
        message_api.send_text_message(target, "No update~")
        return

    notify_added_jobs(added_jobs)
    update_added_jobs_in_db(added_jobs)

    notify_removed_jobs(removed_jobs)
    update_removed_jobs_in_db(removed_jobs)

def notify_added_jobs(added_jobs):
    print('added jobs: ' + str(added_jobs))
    for job_title in added_jobs:
        job_detail = get_job_detail_from_local(job_title)
        text = u"{} from {} is added.\nurl: {}" \
            .format(job_detail['job_title'], job_detail['company_name'], job_detail['job_link'])
        message_api.send_text_message(target, text)

def update_added_jobs_in_db(added_jobs):
    for job_title in added_jobs:
        job_detail = get_job_detail_from_local(job_title)
        job = JobItem({'job_title': job_title, 'company_name': job_detail['company_name'], 'job_link': job_detail['job_link']})
        dao.add_job(job)

def notify_removed_jobs(removed_jobs):
    print('removed jobs: ' + str(removed_jobs))
    for job_title in removed_jobs:
        job_detail = get_job_detail_from_db(job_title)
        text = u"{} from {} is removed." \
            .format(job_detail['job_title'], job_detail['company_name'])
        message_api.send_text_message(target, text)

def update_removed_jobs_in_db(removed_jobs):
    for job_title in removed_jobs:
    	job = JobItem({'job_title': job_title})
    	dao.delete_job(job)

def get_job_detail_from_local(job_title):
    for job in latest_job_items:
        if job['job_title'] == job_title:
            return job

def get_job_detail_from_db(job_title):
    return dao.query_job_by_title(job_title)

compare()

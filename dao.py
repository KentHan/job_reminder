# -*- coding: utf-8 -*-

import os

from pymongo import MongoClient
from job_update_bot.spiders.items import JobItem

# from event import Event
# from util import Util

mongodb_id = os.getenv("MONGODB_ID")
mongodb_pw = os.getenv("MONGODB_PW")
mongodb_uri = os.getenv("MONGODB_URI")

class JobDAO():
	def __init__(self, client=None):
		if client is None:
			self.client = MongoClient(mongodb_uri)
			self.client.admin.authenticate(mongodb_id, mongodb_pw, mechanism='SCRAM-SHA-1')
		else:
			self.client = client
		self.db = self.client.user_data

	def query_all_jobs(self):
		cursor = self.db.job.find()
		return list(cursor)

	def add_job(self, job):
		result = self.db.job.insert_one(
            {
                "job_title": job['job_title']
            }
        )
		return result.acknowledged

	def delete_job(self, job):
		result = self.db.job.delete_one(
            {
                "job_title": job['job_title']
            }
        )
		return result.acknowledged

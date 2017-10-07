import scrapy
import os

from .items import JobItem
import logging

SELECTOR_JOB_TITLE="#intro > form  ul > li:nth-child(3) > div > a::text"
SELECTOR_OTHER_PAGE_LINK_TEXT="#paging > a::text"

class JobSpider(scrapy.Spider):
    name = 'job_update_bot'
    start_urls = os.getenv("JOB_URLS").split(",")

    def parse(self, response):
        logging.info("response.url: " + response.url)
        other_page_link_texts = response.css(SELECTOR_OTHER_PAGE_LINK_TEXT)
        if other_page_link_texts:
        	for index in other_page_link_texts:
        		page_index = index.extract()
        		if page_index.isdigit():
		        	url = response.url + "&page={}".format(page_index)
		        	logging.info('next page: {}'.format(url))
		        	yield scrapy.Request(url, callback=self.parse_job)
        yield scrapy.Request(response.url, callback=self.parse_job)
        
    def parse_job(self, response):
	    for title in response.css(SELECTOR_JOB_TITLE):
	    	item = JobItem()
	    	item['job_title'] = title.extract().strip()
	    	print(item['job_title'])
	    	yield item
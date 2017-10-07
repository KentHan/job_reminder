import scrapy
import os

from .items import JobItem
import logging

SELECTOR_JOB_LINK="#intro > form  ul > li:nth-child(3) > div > a"
SELECTOR_OTHER_PAGE_LINK_TEXT="#paging > a::text"
SELECTOR_COMPANY_NAME="#comp_header > ul > li.comp_name > h1::text"

ONE_ZERO_FOUR_FQDN='https://www.104.com.tw/'

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
        company_name = response.css(SELECTOR_COMPANY_NAME)[0].extract().strip()
        for element in response.css(SELECTOR_JOB_LINK):
            item = JobItem()

            item['job_title'] = element.css('::text')[0].extract().strip()
            print(item['job_title'])

            relative_job_link = element.css('::attr(href)')[0].extract().strip()
            item['job_link'] = ONE_ZERO_FOUR_FQDN + relative_job_link

            item['company_name'] = company_name
            yield item
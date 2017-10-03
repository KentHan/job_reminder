import scrapy

from items import JobItem

SELECTOR_JOB_TITLE="#intro > form  ul > li:nth-child(3) > div > a::text"
SELECTOR_NEXT_PAGE="#paging > a.pn"

class JobSpider(scrapy.Spider):
    name = 'job_update_bot'
    # allowed_domains = ['ptt.cc']
    start_urls = ('https://www.104.com.tw/jobbank/custjob/index.php?r=cust&j=553f4770393b436c35373f683d433b1e12e2e2e7146713f2634j53&page=1', 
    			  'https://www.104.com.tw/jobbank/custjob/index.php?r=cust&j=553f4770393b436c35373f683d433b1e12e2e2e7146713f2634j53&page=2' )

    def parse(self, response):
        # filename = response.url.split('/')[-2] + '.html'
        # with open(filename, 'wb') as f:
        #     f.write(response.body)
        # next_page = response.css(SELECTOR_NEXT_PAGE)
        # if next_page:
        # 	url = response.urljoin(next_page[0].extract())
        # 	print('next page: {}'.format(url))
        # 	yield scrapy.Request(url, self.parse)

        for title in response.css(SELECTOR_JOB_TITLE):
        	item = JobItem()
        	item['job_title'] = title.extract()
        	print(title.extract())
        	yield item
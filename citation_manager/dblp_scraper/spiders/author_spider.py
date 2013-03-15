from scrapy.spider import BaseSpider

class AuthorSpider(BaseSpider):
	name = 'author'
	allowed_domains = ['dblp.org']
	start_urls = ['http://dblp.uni-trier.de/search/author']

	def parse(self, response):
		print response.body
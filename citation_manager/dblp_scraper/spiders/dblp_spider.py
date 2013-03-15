from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector
from dblp_scraper.items import DblpScraperItem, find_authors

from models import PubAuthor

class DBLPSpider(BaseSpider):
	name = 'dblp'
	allowed_domains = ['dblp.org']
	start_urls = [
		'http://www.dblp.org/search/api/?q=ce:author:william_d_smart*&h=1000&c=4&f=0&format=xml' # fill this in programatically
	]

	def parse(self, request):
		hxs = HtmlXPathSelector(request)
		for hit in hxs.select('//hit'):
			item = DblpScraperItem()
			for attr, (selector, func) in item.mappings.iteritems():
				item[attr] = func(hit.select(selector).extract())
			print 'Adding ', item['title']

			# need to do this by hand so we have access to the instance for adding authors
			modelargs = dict((k, item.get(k)) for k in item._values if k in item._model_fields)
			instance = item.django_model(**modelargs)

			instance.save()
			for n, author in enumerate(find_authors(hit.select('descendant::author/text()').extract())):
				author.save()
				pa = PubAuthor(author=author, publication=instance, author_num=n)
				pa.save()
				# import pdb; pdb.set_trace()
				# instance.authors.add(author)
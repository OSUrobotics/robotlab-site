from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector
from dblp_scraper.items import DblpScraperItem, find_authors
import django.db.utils
from models import PubAuthor, Author

from django.template.defaultfilters import slugify as _slugify
def slugify(text):
	return _slugify(text).replace('-','_')

class DBLPSpider(BaseSpider):
	name = 'dblp'
	allowed_domains = ['dblp.org']
	url_format = 'http://www.dblp.org/search/api/?q=ce:author:%s*&h=1000&c=4&f=0&format=xml'
	start_urls = []
	# 	'http://www.dblp.org/search/api/?q=ce:author:william_d_smart*&h=1000&c=4&f=0&format=xml' # fill this in programatically
	# ]

	def __init__(self, *args, **kwargs):
		super(DBLPSpider, self).__init__(*args, **kwargs)
		# import pdb; pdb.set_trace()
		for author in Author.objects.filter(user_id__isnull=False):
			self.start_urls.append(self.url_format % slugify(author.published_name))

	def parse(self, request):
		hxs = HtmlXPathSelector(request)
		for hit in hxs.select('//hit'):
			item = DblpScraperItem()
			for attr, (selector, func) in item.mappings.iteritems():
				item[attr] = func(hit.select(selector).extract())
			# need to do this by hand so we have access to the instance for adding authors
			# import pdb; pdb.set_trace()
			modelargs = dict((k, item.get(k)) for k in item._values if k in item._model_fields)
			instance = item.django_model(**modelargs)
			try:
				instance.save()
				print 'Adding ', item['title']
			except django.db.utils.IntegrityError, e:
				# ignore things we've already imported
				continue
			for n, author in enumerate(find_authors(hit.select('descendant::author/text()').extract())):
				author.save()
				pa = PubAuthor(author=author, publication=instance, author_num=n)
				pa.save()
				# import pdb; pdb.set_trace()
				# instance.authors.add(author)

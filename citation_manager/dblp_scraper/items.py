# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/topics/items.html

from scrapy.item import Item, Field
from scrapy.contrib.djangoitem import DjangoItem
from models import Publication, Author

def find_authors(authors):
    return [Author.from_dblp(name) for name in authors]

def delistify(l):
    return l[0].strip() if l else None

def noop(i):
    return i

def get_key(l):
    return l[0].split('/')[-1].strip()

class DblpScraperItem(DjangoItem):
    django_model = Publication
    mappings = dict(
		dblp_id		= ('@id',							delistify),
		title		= ('descendant::title/text()', 		delistify),
		doi			= ('descendant::title/@ee', 		delistify),
		venue		= ('descendant::venue/text()',		delistify),
		venue_url	= ('descendant::venue/@url',		delistify),
		pages		= ('descendant::venue/@pages',		delistify),
		journal		= ('descendant::venue/@journal',	delistify),
		conference	= ('descendant::venue/@conference',	delistify),
		number		= ('descendant::venue/@number',		delistify),
		volume		= ('descendant::venue/@volume',		delistify),
		year		= ('descendant::year/text()',		delistify),
		type		= ('descendant::type/text()',		delistify),
        key         = ('descendant::url/text()',        get_key),
	)
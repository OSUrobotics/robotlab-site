from django.db import models
from django.contrib.auth.models import User, Group

from pybtex.database import Entry, Person
from pybtex.style import FormattedBibliography
from pybtex.plugin import find_plugin

import bibtex_constants

from cms.models import CMSPlugin

class Video(models.Model):
	embed_url = models.URLField()
	class Meta:
		app_label = 'citation_manager'

class Author(models.Model):
	user_id = models.ForeignKey(User, null=True, blank=True)
	google_scholar_id = models.CharField(max_length=12, null=True, blank=True)
	dblp_id = models.CharField(max_length=255)
	published_name = models.CharField(max_length=255)

	def to_pybtex(self):
		return Person(self.published_name)

	def __unicode__(self):
		return self.published_name

	class Meta:
		app_label = 'citation_manager'

	@property
	def dblp_author(self):
		parts = self.dblp_id.split()
		return '%s:%s' % (parts[-1], '_'.join([p.strip('.') for p in parts[:-1]]))

	@property
	def dblp_link(self):
		letter = self.dblp_id.split()[-1][0].lower()
		return 'http://www.dblp.org/db/indices/a-tree/%s/%s=.html' % (letter, self.dblp_author)

	@staticmethod
	def from_dblp(name):
		author = Author.objects.filter(published_name=name)
		if author:
			return author[0]
		else:
			return Author(dblp_id=name, published_name=name)

class Publication(models.Model):
	dblp_id		= models.IntegerField(null=True, blank=True)
	title		= models.TextField()
	doi			= models.URLField(null=True,blank=True)
	authors		= models.ManyToManyField(Author, through='PubAuthor')
	venue		= models.CharField(null=True,max_length=255, blank=True)
	venue_url	= models.CharField(null=True,max_length=255, blank=True)
	# venue_type	= models.TextField() # FIXME!
	pages		= models.CharField(null=True,max_length=20 , blank=True)
	conference	= models.CharField(null=True,max_length=255, blank=True)
	journal		= models.CharField(null=True,max_length=255, blank=True)
	number		= models.IntegerField(null=True, blank=True)
	volume		= models.CharField(null=True,max_length=255, blank=True)
	year		= models.IntegerField(null=True, blank=True)
	type		= models.CharField(max_length=255, choices=zip(bibtex_constants.entry_types, bibtex_constants.entry_types))
	key			= models.CharField(max_length=255)
	abstract	= models.TextField(null=True,blank=True)
	groups		= models.ManyToManyField(Group, null=True, blank=True)
	hidden		= models.BooleanField(default=False)
	videos      = models.ManyToManyField(Video, null=True, blank=True)

	def __unicode__(self):
		return self.title

	@property
	def fields(self):
		fields = dict()
		for k in self._meta.get_all_field_names():
			if k != 'pubauthor':
				v = getattr(self, k)
				if v:
					fields[k] = unicode(v)
		if self.conference:
			fields['booktitle'] = self.conference
		del fields['authors']
		fields['year'] = unicode(fields['year'])
		return fields

	def to_pybtex(self):
		fields = self.fields
		
		entry = Entry(self.type, fields=fields, persons=dict(author=[p.to_pybtex() for p in self.authors.all()]))
		entry.key = self.key
		return entry

	def export(self, backend):
		output_backend = find_plugin('pybtex.backends', backend)
		style_cls = find_plugin('pybtex.style.formatting', 'plain')
		style = style_cls()
		formatted_entries = style.format_entries([self.to_pybtex()])
		# formatted_bibliography = FormattedBibliography([e for e in formatted_entries], style)
		ob = output_backend(None)
		return formatted_entries.next().text.render(ob)

	def html(self):
		return self.export('html')

	def plaintext(self):
		return self.export('plaintext')

	class Meta:
		unique_together = (('doi', 'title'))
		app_label = 'citation_manager'

class PubAuthor(models.Model):
	author = models.ForeignKey(Author)
	publication = models.ForeignKey(Publication)
	author_num = models.PositiveSmallIntegerField()
	# maybe add author type (author/editor)

	def __unicode__(self):
		return self.author.__unicode__() + ' on ' + self.publication.__unicode__()

	class Meta:
		app_label = 'citation_manager'
		ordering = ['author_num']

class GroupInfo(models.Model):
	group = models.OneToOneField(Group)
	type  = models.CharField(max_length=255, choices=([
		('lab','lab'),
		('project','project'),
	]))
	description = models.TextField(null=True, blank=True)
	videos      = models.ManyToManyField(Video, null=True, blank=True)

	class Meta:
		app_label = 'citation_manager'

class PublicationPlugin(CMSPlugin):
	user  = models.ForeignKey(User, related_name='pub_plugin', null=True, blank=True)
	group = models.ForeignKey(Group, related_name='pub_plugin', null=True, blank=True)

	def get_pubs(self):
		owner = self.user and self.user or self.group
		if type(owner) == User:
			return Publication.objects.filter(authors__user_id=owner, hidden=False).order_by('-year')
		elif type(owner) == Group:
			return owner.publication_set.order_by('-year')

	def __unicode__(self):
		return u'Publications'

class GroupMembershipPlugin(CMSPlugin):
	type  = models.CharField(max_length=255, choices=([
		('lab','lab'),
		('project','project'),
	]))
	person = models.ForeignKey(User, related_name='plugins')

	def __unicode__(self):
		return u'Groups'

class PublishedAsPlugin(CMSPlugin):
	person = models.ForeignKey(User, related_name='pub_as_plugin', null=True, blank=True)

	def __unicode__(self):
		return u'PublishedAs: ' + self.person.get_full_name()
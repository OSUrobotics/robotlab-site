from django.http import HttpResponse
from django.template import Context, loader
from django.views.generic import ListView

import models
import bibtex_constants

class PublicationViewList(ListView):
	model = models.Publication

	def get_context_data(self, **kwargs):
		context = super(PublicationViewList, self).get_context_data(**kwargs)
		context['pubs'] = models.Publication.objects.order_by('-year')
		return context

def publications(request):
	pubs = models.Publication.objects.order_by('-year')
	template = loader.get_template('citation_manager/publications.html')
	context = Context({
		'pubs': pubs,
	})
	return HttpResponse(template.render(context))

def publication(request, *args):
	pid = args[0]
	pub = models.Publication.objects.get(key=pid)
	template = loader.get_template('citation_manager/publication.html')
	context = Context({
		'pub': pub,
		'projects': pub.groups.filter(groupinfo__type='project'),
		'labs': pub.groups.filter(groupinfo__type='lab'),
	})
	return HttpResponse(template.render(context))

def person(request, user_id):
	pubs = models.Publication.objects.filter(authors__user_id=user_id).order_by('-year')
	template = loader.get_template('citation_manager/person.html')
	user = models.User.objects.get(pk=user_id)
	context = Context({
		'person': user,
		'pubs': pubs,
		'projects': user.groups.filter(groupinfo__type='project'),
	})
	return HttpResponse(template.render(context))

def group(request, group_id):
	pubs = models.Group.objects.get(pk=group_id).publication_set.order_by('-year')
	template = loader.get_template('citation_manager/group.html')
	context = Context({
		'group': models.Group.objects.get(pk=group_id),
		'pubs': pubs,
	})
	return HttpResponse(template.render(context))


def bibtex(request, *args):
	pub = models.Publication.objects.get(key=args[0])
	template = loader.get_template('citation_manager/bibtex.bib')
	fields = {}
	for f in bibtex_constants.fields:
		if hasattr(pub, f) and getattr(pub, f):
			fields[f] = getattr(pub, f)
	if 'booktitle' not in fields and pub.conference:
		fields['booktitle'] = pub.conference
	context = Context({
		'pub': pub,
		'fields': fields,
		'authors': [a.published_name for a in pub.authors.all()]
	})
	return HttpResponse(template.render(context),content_type="text/plain")

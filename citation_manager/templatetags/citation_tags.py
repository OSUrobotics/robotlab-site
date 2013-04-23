from django import template
from django.template.defaultfilters import stringfilter
from django.core import urlresolvers
from citation_manager import models

register = template.Library()

@register.filter(is_safe=True)
@stringfilter
def author_links(text):
	text = text.replace('&nbsp;', ' ')
	for author in models.Author.objects.filter(user_id__isnull=False):
		author_page = urlresolvers.reverse('person', args=(author.user_id.pk,))
		text = text.replace(author.published_name, '<a href="%s">%s</a>' % (author_page, author.published_name))
	return text

@register.inclusion_tag('citation_manager/includes/publications.html')
def list_publications(pubs):
	return {'pubs':pubs}
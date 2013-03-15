from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
import citation_manager.views
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'robotlab.views.home', name='home'),
    # url(r'^robotlab/', include('robotlab.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),

    # url(r'^publications/?$',	citation_manager.views.publications,name='publications'),
    url(r'^publications/?$',	citation_manager.views.PublicationViewList.as_view() ,name='publications'),
    url(r'^project/(.+)?$',		citation_manager.views.group,		name='group'),
    url(r'^person/(?P<user_id>\d+)/$',		citation_manager.views.person,		name='person'),
    url(r'^publication/(.+)?$',	citation_manager.views.publication,	name='publication'),
    url(r'^bibtex/(.+)?$', 		citation_manager.views.bibtex,		name='bibtex'),

    url(r'^', include('cms.urls')),
)

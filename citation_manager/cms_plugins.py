from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
from citation_manager.models import PublicationPlugin as PublicationPluginModel
from citation_manager.models import GroupMembershipPlugin as GroupMembershipPluginModel
from citation_manager.models import PublishedAsPlugin as PublishedAsPluginModel
from django.utils.translation import ugettext as _

class PublicationPlugin(CMSPluginBase):
	model = PublicationPluginModel
	name = _('Publication List')
	render_template = 'citation_manager/includes/publications.html'

	def render(self, context, instance, placeholder):
		context.update({
			'pubs':instance.get_pubs(),
		})
		return context

plugin_pool.register_plugin(PublicationPlugin)

class GroupMembershipPlugin(CMSPluginBase):
	model = GroupMembershipPluginModel
	name = _('Membership')
	render_template = 'citation_manager/includes/group_membership.html'

	def render(self, context, instance, placeholder):
		context.update({
			'groups': instance.person.groups.filter(groupinfo__type=instance.type)
		})
		return context

plugin_pool.register_plugin(GroupMembershipPlugin)

class PublishedAsPlugin(CMSPluginBase):
	model = PublishedAsPluginModel
	name = _('Published As')
	render_template = 'citation_manager/includes/published_as.html'

	def render(self, context, instance, placeholder):
		context.update({
			'person': instance.person,
		})
		return context

plugin_pool.register_plugin(PublishedAsPlugin)

from django.contrib import admin
from citation_manager.models import Author, Publication, GroupInfo, Group
from django.contrib.auth.admin import GroupAdmin


admin.site.register(Author)
admin.site.register(Publication)
# admin.site.register(PubAuthor)

class GroupInline(admin.StackedInline):
	model = GroupInfo
	can_delete = True
	verbose_name_plural = 'group info'

class GroupAdmin(GroupAdmin):
	inlines = (GroupInline,)

admin.site.unregister(Group)
admin.site.register(Group, GroupAdmin)
from django.contrib import admin
from citation_manager.models import Author, Publication, GroupInfo, Group, User
from django.contrib.auth.admin import GroupAdmin, UserAdmin


admin.site.register(Author)
admin.site.register(Publication)
# admin.site.register(PubAuthor)

class GroupInline(admin.StackedInline):
	model = GroupInfo
	can_delete = True
	verbose_name_plural = 'group info'

class GroupAdmin(GroupAdmin):
	inlines = (GroupInline,)

class UserInline(admin.StackedInline):
	model = Author
	can_delete = True

class UserAdmin(UserAdmin):
	inlines = (UserInline,)

admin.site.unregister(Group)
admin.site.register(Group, GroupAdmin)

admin.site.unregister(User)
admin.site.register(User, UserAdmin)
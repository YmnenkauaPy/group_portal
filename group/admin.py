from django.contrib import admin
from group.models import Group, ForumThread, ForumPost

admin.site.register(Group)
admin.site.register(ForumThread)
admin.site.register(ForumPost)
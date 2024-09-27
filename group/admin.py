from django.contrib import admin
from group.models import Group, ForumThread, ForumPost, Subject, Grade, ReportCard

admin.site.register(Group)
admin.site.register(ForumThread)
admin.site.register(ForumPost)
admin.site.register(Subject)
admin.site.register(Grade)
admin.site.register(ReportCard)
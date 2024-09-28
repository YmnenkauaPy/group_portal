from django.contrib import admin
from gradebook.models import Subject, Grade, ReportCard

admin.site.register(Subject)
admin.site.register(Grade)
admin.site.register(ReportCard)
from django.db import models
from django.conf import settings

    
class Group(models.Model):
    title = models.CharField(max_length=40, unique=True)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    members = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="member_of_groups")
    admin = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="admin_groups")
    
    def __str__(self):
        return self.title
    
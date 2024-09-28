from django.db import models
from authentication.models import CustomUser

    
class Group(models.Model):
    title = models.CharField(max_length=40, unique=True)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    members = models.ManyToManyField(CustomUser, related_name="member_of_groups")
    admin = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="admin_groups")
    
    def __str__(self):
        return self.title
    
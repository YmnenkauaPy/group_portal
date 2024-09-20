from django.db import models
from django.contrib.auth.models import User

class CustomUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    details = models.CharField(max_length=100, default='')
    profile_picture = models.ImageField(upload_to='profile_media/', blank=True, null=True)
    status = models.CharField(max_length=30, default='member')

    def __str__(self):
        return self.user.username 
    
class Group(models.Model):
    title = models.CharField(max_length=40, unique=True)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    members = models.ManyToManyField(CustomUser, related_name="member_of_groups")
    admin = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="admin_groups")
    
    def __str__(self):
        return self.title
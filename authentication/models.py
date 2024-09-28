from django.db import models
from django.contrib.auth.models import User

class CustomUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    details = models.CharField(max_length=100, default='')
    profile_picture = models.ImageField(upload_to='profile_media/', blank=True, null=True)
    status = models.CharField(max_length=30, default='member')

    def __str__(self):
        return self.user.username 

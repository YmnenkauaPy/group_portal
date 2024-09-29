from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    details = models.CharField(max_length=100, default='')
    profile_picture = models.ImageField(upload_to='profile_media/', blank=True, null=True)
    status = models.CharField(max_length=30, default='member')
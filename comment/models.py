from django.db import models
from forum.models import ForumThread
from django.conf import settings

class Comment(models.Model):
    thread = models.ForeignKey(ForumThread, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    media = models.FileField(upload_to = "comments_media/", blank=True, null=True)

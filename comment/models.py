from django.db import models
from forum.models import ForumThread
from django.contrib.auth.models import User

class Comment(models.Model):
    thread = models.ForeignKey(ForumThread, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    media = models.FileField(upload_to = "comments_media/", blank=True, null=True)

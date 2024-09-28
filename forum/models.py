from django.db import models
from django.contrib.auth.models import User

class ForumThread(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField(null=True) 
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
    
class ForumPost(models.Model):
    thread = models.ForeignKey(ForumThread, related_name = "posts", on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.author} - {self.thread.title}'
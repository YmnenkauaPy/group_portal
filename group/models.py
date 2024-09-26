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

class Comment(models.Model):
    thread = models.ForeignKey(ForumThread, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    media = models.FileField(upload_to = "comments_media/", blank=True, null=True)

class Like(models.Model):
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name='likes')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='liked_comments')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('comment', 'user')

class Event(models.Model):
    name = models.CharField(max_length=40)
    description = models.TextField()
    day_month_year = models.DateField()
    time = models.TimeField()
    #group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name="group") №нужно будет прикреплять евенты к группам, когда они появятся
    
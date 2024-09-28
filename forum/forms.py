from django import forms
from forum import models
from forum.models import ForumThread

class ForumThreadForm(forms.ModelForm):
    class Meta:
        model = models.ForumThread
        fields = ['title', 'content']
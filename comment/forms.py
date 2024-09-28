from django import forms
from comment import models

class CommentForm(forms.ModelForm):
    class Meta:
        model = models.Comment
        fields = ['content', 'media']
        widgets = {
            'content': forms.Textarea(),
            "media": forms.FileInput(),
        }
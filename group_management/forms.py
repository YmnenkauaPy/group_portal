from django import forms
from group import models

class GroupForm(forms.ModelForm):
    class Meta:
        model = models.Group
        fields = ['title', 'description', 'members']
        
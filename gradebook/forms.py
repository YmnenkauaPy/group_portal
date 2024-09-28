from django import forms
from gradebook import models

class GradeForm(forms.ModelForm):
    class Meta:
        model = models.Grade
        fields = ['student', 'subject', 'grade']

from django import forms
from event import models

class EventForm(forms.ModelForm):
    class Meta:
        model = models.Event
        fields = ['name', 'description', 'day_month_year', 'time']
        widgets = {
            'day_month_year': forms.DateInput(attrs={'readonly': True,}),
            'time': forms.TimeInput(attrs={'type': 'time'}),         
        }

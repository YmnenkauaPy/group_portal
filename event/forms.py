from django import forms
from event.models import Event
from group.models import Group
from django.db.models import Q

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['name', 'description', 'day_month_year', 'time', 'group']
        widgets = {
            'day_month_year': forms.DateInput(attrs={'readonly': True,}),
            'time': forms.TimeInput(attrs={'type': 'time'}),         
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(EventForm, self).__init__(*args, **kwargs)

        if self.user:
            available_groups = Group.objects.filter(
                Q(members=self.user) | Q(admin=self.user)
            ).distinct()

            self.fields['group'].queryset = available_groups
            
            if available_groups.exists():
                self.fields['group'].initial = available_groups.first()
                
            self.fields['group'].empty_label = None
            self.fields['group'].required = True
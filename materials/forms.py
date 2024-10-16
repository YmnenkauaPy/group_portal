from django import forms
from materials import models
from django.db.models import Q
from group.models import Group

class MaterialForm(forms.ModelForm):
    class Meta:
        model = models.Material
        fields = ['name', 'content', 'group']
        widgets = {
            "content": forms.FileInput(),
        }
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(MaterialForm, self).__init__(*args, **kwargs)

        if self.user:
            available_groups = Group.objects.filter(
                Q(members=self.user) | Q(admin=self.user) | Q(moderators=self.user)
            ).distinct()
            
            self.fields['group'].queryset = available_groups
            
            if available_groups.exists():
                self.fields['group'].initial = available_groups.first()
                
            self.fields['group'].empty_label = None
            self.fields['group'].required = True
from django import forms
from authentication.models import CustomUser
from django.contrib.auth.forms import UserCreationForm

class CustomUserForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = UserCreationForm.Meta.fields + ("details", "profile_picture", "role" )
        widgets = {
            'profile_picture': forms.FileInput(),
        }

        role = forms.ChoiceField(
        choices=CustomUser.ROLE_CHOICES,
        label="Role",
        initial='user',
    )
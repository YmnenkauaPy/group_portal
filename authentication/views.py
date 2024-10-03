from django.shortcuts import render
from authentication import forms
from django.shortcuts import redirect, render
from django.contrib.auth import login

def register(request):
    if request.method == 'POST':
        custom_user_form = forms.CustomUserForm(request.POST, request.FILES)
        
        if custom_user_form.is_valid():
            custom_user = custom_user_form.save()
            custom_user.save() 

            login(request, custom_user)
            return redirect('group_list')
    else:
        custom_user_form = forms.CustomUserForm()

    return render(request, 'registration/register.html', {'custom_user_form': custom_user_form})
    
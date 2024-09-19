from django.shortcuts import get_object_or_404, redirect, render
from group import models
from django.contrib.auth import login
from group import forms

def group_list(request):
    groups = models.Group.objects.all()
    return render(request, 'group/group_list.html', {'groups': groups})

def group_detail(request, pk):
    group = get_object_or_404(models.Group, pk=pk)
    return render(request, 'group/group_detail.html', {'group': group})


def register(request):
    if request.method == 'POST':
        user_form = forms.RegisterForm(request.POST)
        custom_user_form = forms.CustomUserForm(request.POST, request.FILES)
        
        if user_form.is_valid() and custom_user_form.is_valid():
            user = user_form.save() 
            custom_user = custom_user_form.save(commit=False)
            custom_user.user = user  
            custom_user.save() 

            login(request, user)
            return redirect('group_list')
    else:
        user_form = forms.RegisterForm()
        custom_user_form = forms.CustomUserForm()

    return render(request, 'registration/register.html', {'user_form': user_form, 'custom_user_form': custom_user_form})
    

def profile_view(request):
    user = request.user
    custom_user = models.CustomUser.objects.get(user=user) 

    time_joined = user.date_joined #UTC

    return render(request, 'group/profile_view.html', {'custom_user': custom_user, 'time':time_joined})
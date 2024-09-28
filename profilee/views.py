from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from authentication import models
from profilee import forms


@login_required(login_url='/login/')
def profile_view(request):
    user = request.user
    custom_user = models.CustomUser.objects.get(user=user) 

    time_joined = user.date_joined

    return render(request, 'group/profile_view.html', {'custom_user': custom_user, 'time':time_joined})

def update_profile(request):
    user = request.user
    if request.method == 'POST':
        form = forms.ProfileForm(request.POST, request.FILES, instance=user.customuser)
        
        if form.is_valid():
            profile = form.save(commit=False)
            
            user.username = form.cleaned_data['username']
            user.save() 
            profile.save() 
            
            return redirect('profile_view')
    else:
        form = forms.ProfileForm(instance=user.customuser, initial={'username': user.username})

    return render(request, 'group/update_profile.html', {'form': form})


from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from authentication import models
from profilee import forms


@login_required(login_url='/login/')
def profile_view(request):
    user = models.CustomUser.objects.get(username=request.user.username)

    return render(request, 'group/profile_view.html', {'custom_user': user})

def update_profile(request):
    user = request.user
    user = models.CustomUser.objects.get(username=request.user.username)
    if request.method == 'POST':
        form = forms.ProfileForm(request.POST, request.FILES, instance=user)
        
        if form.is_valid():
            profile = form.save(commit=False)
            
            user.username = form.cleaned_data['username']
            user.save() 
            profile.save() 
            
            return redirect('profile_view')
    else:
        form = forms.ProfileForm(instance=user)

    return render(request, 'group/update_profile.html', {'form': form})


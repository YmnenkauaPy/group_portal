from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from authentication.models import CustomUser
from group.models import Group
from profilee import forms
from django.db.models import Q


@login_required(login_url='/login/')
def profile_view(request):
    user = CustomUser.objects.get(username=request.user.username)
    groups = Group.objects.filter(
    Q(admin=user) | Q(moderators=user) | Q(members=user)).distinct()

    user_roles = []
    for group in groups:
        if user == group.admin:
            role = 'Admin'
        elif user in group.moderators.all():
            role = 'Moderator'
        elif user in group.members.all():
            role = 'Member'
        else:
            role = 'Not a member'
        user_roles.append({'group': group, 'role': role})
    
    return render(request, 'group/profile_view.html', {'custom_user':user, 'user_roles': user_roles})

def update_profile(request):
    user = request.user
    user = CustomUser.objects.get(username=request.user.username)
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


from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from group_management import forms
from authentication.models import CustomUser
from group import models
from django.db.models import Q

@login_required
def add_group(request):
    if request.method == 'POST':
        form = forms.GroupForm(request.POST)
        if form.is_valid():
            group = form.save(commit=False)
            group.admin = request.user 
            group.save()
            form.save_m2m()

            user = request.user 
            user.is_staff = True
            user.is_superuser = True
            user.save()

            return redirect('group_list')
    else:
        form = forms.GroupForm()
    return render(request, 'group_management/add_group.html', {'form': form})

def update_group(request, pk):
    group = get_object_or_404(models.Group, pk=pk)
    if request.method == 'POST':
        form = forms.GroupForm(request.POST, request.FILES, instance=group)
        if form.is_valid():
            form.save()
            return redirect('group_detail', pk=group.pk)
    else:
        form = forms.GroupForm(instance=group)
    return render(request, 'group_management/update_group.html', {'form': form, 'group': group})


def delete_group(request, pk):
    group = get_object_or_404(models.Group, pk=pk)
    if request.method == 'POST':
        user = request.user
        group.delete() 
        user_has_groups = models.Group.objects.filter(
            Q(admin=user) | Q(moderators=user) | Q(members=user)
        ).exists()

        if not user_has_groups:
            user.is_staff = False
            user.is_superuser = False
            user.save()

        return redirect('group_list') 
    return render(request, 'group_management/delete_group.html', {'group': group})

def add_moderator(request, group, user):
    group = get_object_or_404(models.Group, pk=group)
    user = get_object_or_404(CustomUser, pk=user)
    group.moderators.add(user)

    return redirect('group_detail', pk=group.pk)

def remove_moderator(request, group, user):
    group = get_object_or_404(models.Group, pk=group)
    user = get_object_or_404(CustomUser, pk=user)
    
    group.moderators.remove(user)
    
    return redirect('group_detail', pk=group.pk)
    
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from group_management import forms
from authentication.models import CustomUser
from group import models
from django.http import JsonResponse
from django.db.models import Q

def search_users(request):
    if request.method == 'GET':
        query = request.GET.get('q', '') 
        if query:
            users = CustomUser.objects.filter(username__icontains=query).exclude(id=request.user.id)
            user_list = [{"id": user.id, "username": user.username} for user in users]
            return JsonResponse({"users": user_list})
    return JsonResponse({"users": []})  

def add_member(request, group):
    group_ = get_object_or_404(models.Group, pk=group)
    selected_user_ids = request.POST.get('selected_users', '')
    user_ids = selected_user_ids.split(',') if selected_user_ids else []
    user_ids = [int(user_id) for user_id in user_ids if user_id.isdigit()]

    users = CustomUser.objects.filter(id__in=user_ids).exclude(id=request.user.id)

    for user in users:
        group_.members.add(user)

    return redirect('group_detail', pk=group)

def delete_member(request, group, user):
    group = get_object_or_404(models.Group, pk=group)
    user = get_object_or_404(CustomUser, pk=user)
    
    group.members.remove(user)
    
    return redirect('group_detail', pk=group.pk)


@login_required
def add_group(request):
    form = forms.GroupForm()  

    if request.method == 'POST':
        form = forms.GroupForm(request.POST)
        if form.is_valid():
            group = form.save(commit=False)
            group.admin = request.user 
            group.save()

            selected_user_ids = request.POST.get('selected_users', '')
            user_ids = selected_user_ids.split(',') if selected_user_ids else []

            user_ids = [int(user_id) for user_id in user_ids if user_id.isdigit()]

            users = CustomUser.objects.filter(id__in=user_ids)
            group.members.set(users)
            
            user = request.user 
            user.is_staff = True
            user.is_superuser = True
            user.save()

            return redirect('group_list', page=1)

    return render(request, 'group_management/add_group.html', {'form':form})

    
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

        return redirect('group_list', page=1) 
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
    
from django.shortcuts import render
from group.models import Group
from authentication.models import CustomUser
from django.db.models import Q

def group_list(request):
    if not request.user.is_authenticated:
        groups = []
    else:
        user = CustomUser.objects.get(username=request.user.username)
        groups = Group.objects.filter(Q(admin=user) | Q(moderators=user) | Q(members=user)).distinct()

    return render(request, 'group/group_list.html', {'groups': groups})

def group_detail(request, pk):
    group = Group.objects.get(pk=pk)
    all_members = group.members.all().union(group.moderators.all())
    
    members_with_roles = []

    for member in all_members:
        role = "Member"
        if member in group.moderators.all():
            role = "Moderator"
        if member == group.admin:
            role = "Admin"
        members_with_roles.append({'user': member, 'role': role})
        
    return render(request, 'group/group_detail.html', {'group': group, 'members_with_roles': members_with_roles})

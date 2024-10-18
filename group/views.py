from django.shortcuts import render
from group.models import Group
from authentication.models import CustomUser
from django.db.models import Q
from django.core.paginator import Paginator

def group_list(request):
    if not request.user.is_authenticated:
        groups = []
    else:
        user = CustomUser.objects.get(pk=request.user.id)
        groups = Group.objects.filter(Q(admin=user) | Q(moderators=user) | Q(members=user)).distinct()

    paginator = Paginator(groups, 5)
    page_number = request.GET.get('page')  
    page_obj = paginator.get_page(page_number)  

    return render(request, 'group/group_list.html', {'page_obj': page_obj})



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

from django.shortcuts import get_object_or_404, redirect, render
from group.models import Group
from django.contrib.auth import login
from group.forms import CustomUserCreationForm

def group_list(request):
    groups = Group.objects.all()
    return render(request, 'group/group_list.html', {'groups': groups})

def group_detail(request, pk):
    group = get_object_or_404(Group, pk=pk)
    return render(request, 'group/group_detail.html', {'group': group})

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('group_list')
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/register.html', {'form':form})


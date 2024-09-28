from django.shortcuts import get_object_or_404, render
from group import models

def group_list(request):
    groups = models.Group.objects.all()
    return render(request, 'group/group_list.html', {'groups': groups})

def group_detail(request, pk):
    group = get_object_or_404(models.Group, pk=pk)
    return render(request, 'group/group_detail.html', {'group': group})

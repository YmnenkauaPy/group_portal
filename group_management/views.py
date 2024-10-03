from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from group_management import forms
from group import models

@login_required
def add_group(request):
    if request.method == 'POST':
        form = forms.GroupForm(request.POST)
        if form.is_valid():
            group = form.save(commit=False)
            group.admin = request.user 
            group.save()
            form.save_m2m()
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
        group.delete() 
        return redirect('group_list') 
    return render(request, 'group_management/delete_group.html', {'group': group})
    
from django.shortcuts import redirect, get_object_or_404, render
from materials import models
from django.db.models import Q
from materials import forms
from group.models import Group

def role_is(user):
    role = 'member'
    if Q(group__admin=user) | Q(group__moderators=user):
        role='not member'
    return role

def materials_list(request):
    materials = models.Material.objects.filter(Q(group__members=request.user) | Q(group__admin=request.user) | Q(group__moderators=request.user))
    role = role_is(request.user)
    return render(request, 'materials/materials_list.html', {'materials': materials, 'role':role})

def add_material(request):
    if request.method == 'POST':
        form = forms.MaterialForm(request.POST, request.FILES, user=request.user)
        if form.is_valid():
            material = form.save(commit=False)
            material.author = request.user
            material.save()
        
            return redirect('materials_list')
    else:
        form = forms.MaterialForm(user=request.user)

    return render(request, 'materials/add_material.html', {'form': form})

def edit_material(request, pk):
    material = get_object_or_404(models.Material, pk=pk)
    groups = Group.objects.filter(Q(members=request.user) | Q(admin=request.user) | Q(moderators=request.user))

    if request.method == 'POST':
        form = forms.MaterialForm(request.POST, request.FILES, instance=material)
        
        if form.is_valid():
            form.save()
            return redirect('materials_list')
        else:
            print(form.errors)
    else:
        form = forms.MaterialForm(instance=material)

    return render(request, 'materials/edit_material.html', {'form': form, 'material': material, 'groups':groups})

def delete_material(request, pk):
    material = get_object_or_404(models.Material, pk=pk)

    if request.method == 'POST':
        material.delete() 
        return redirect('materials_list') 

    return render(request, 'materials/delete_material.html', {'material': material})
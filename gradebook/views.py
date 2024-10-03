from django.shortcuts import get_object_or_404, redirect, render
from django.shortcuts import render
from gradebook.models import Grade
from gradebook.forms import GradeForm
from django.contrib.auth.decorators import login_required


def grades_list(request):
    grades = Grade.objects.all()
    return render(request, 'grades/grades_list.html', {'grades': grades})

@login_required
def add_grade(request):
    if request.method == 'POST':
        form = GradeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('grades_list')
    else:
        form = GradeForm()  
    return render(request, 'grades/add_grade.html', {'form': form})

def edit_grade(request, pk):
    grade = get_object_or_404(Grade, pk=pk)
    if request.method == 'POST':
        form = GradeForm(request.POST, instance=grade)
        if form.is_valid():
            form.save()
            return redirect('grades_list')
    else:
        form = GradeForm(instance=grade)
    return render(request, 'grades/edit_grade.html', {'form': form, 'grade': grade})

def delete_grade(request, pk):
    grade = get_object_or_404(Grade, pk=pk)
    if request.method == "POST":
        grade.delete()
        return redirect('grades_list')
    return render(request, 'grades/delete_grade.html', {"grade":grade})
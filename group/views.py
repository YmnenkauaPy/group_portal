from django.shortcuts import get_object_or_404, redirect, render
from group import models
from group.models import ForumThread, Grade
from django.contrib.auth.models import User
from django.contrib.auth import login
from group import forms
from group.forms import GradeForm
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.urls import reverse_lazy
from datetime import datetime
from django.views.generic import DetailView, CreateView, DeleteView, UpdateView, View 
from django.contrib.auth.decorators import user_passes_test

def group_list(request):
    groups = models.Group.objects.all()
    return render(request, 'group/group_list.html', {'groups': groups})

def group_detail(request, pk):
    group = get_object_or_404(models.Group, pk=pk)
    return render(request, 'group/group_detail.html', {'group': group})


def register(request):
    if request.method == 'POST':
        user_form = forms.RegisterForm(request.POST)
        custom_user_form = forms.CustomUserForm(request.POST, request.FILES)
        
        if user_form.is_valid() and custom_user_form.is_valid():
            user = user_form.save() 
            custom_user = custom_user_form.save(commit=False)
            custom_user.user = user  
            custom_user.save() 

            login(request, user)
            return redirect('group_list')
    else:
        user_form = forms.RegisterForm()
        custom_user_form = forms.CustomUserForm()

    return render(request, 'registration/register.html', {'user_form': user_form, 'custom_user_form': custom_user_form})
    
@login_required(login_url='/login/')
def profile_view(request):
    user = request.user
    custom_user = models.CustomUser.objects.get(user=user) 

    time_joined = user.date_joined

    return render(request, 'group/profile_view.html', {'custom_user': custom_user, 'time':time_joined})

def update_profile(request):
    user = request.user
    if request.method == 'POST':
        form = forms.ProfileForm(request.POST, request.FILES, instance=user.customuser)
        
        if form.is_valid():
            profile = form.save(commit=False)
            
            user.username = form.cleaned_data['username']
            user.save() 
            profile.save() 
            
            return redirect('profile_view')
    else:
        form = forms.ProfileForm(instance=user.customuser, initial={'username': user.username})

    return render(request, 'group/update_profile.html', {'form': form})

def thread_list(request):
    threads = ForumThread.objects.all()
    return render(request, 'forum/thread_list.html', {'threads': threads})

class ThreadDetailView(DetailView):
    model = models.ForumThread
    context_object_name = 'thread'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comment_form'] = forms.CommentForm()
        return context
    
    def post(self, request, *args, **kwargs):
        comment_form = forms.CommentForm(request.POST, request.FILES)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.author = request.user
            comment.thread = self.get_object()
            comment.save()

            return redirect('thread_detail', pk=comment.thread.pk)

@login_required
def thread_create(request):
    if request.method == 'POST':
        form = forms.ForumThreadForm(request.POST)
        if form.is_valid():
            thread = form.save(commit=False)
            thread.author = request.user 
            thread.save()
            return redirect('thread_detail', pk=thread.pk)
    else:
        form = forms.ForumThreadForm()
    
    return render(request, 'forum/thread_create.html', {'form': form})
    
@login_required
def thread_update(request, pk):
    thread = get_object_or_404(ForumThread, pk=pk)
    if request.method == 'POST':
        form = forms.ForumThreadForm(request.POST, instance=thread)
        if form.is_valid():
            form.save()
            return redirect('thread_detail', pk=thread.pk)
    else:
        form = forms.ForumThreadForm(instance=thread)
    return render(request, 'forum/thread_form.html', {'form': form})


class CommentLikeToggle(View):
    def post(self, request, *args, **kwargs):
        comment = get_object_or_404(models.Comment, pk=self.kwargs.get('pk'))
        like_qs = models.Like.objects.filter(comment=comment, user=request.user)
        liked = False
        if like_qs.exists():
            like_qs.delete()
        else:
            models.Like.objects.create(comment=comment, user=request.user)
            liked = True
        
        return JsonResponse({
            'liked': liked,
            'likes_count': comment.likes.count(),
        })

def edit_comment(request, pk):
    comment = get_object_or_404(models.Comment, pk=pk)

    if request.method == 'POST':
        form = forms.CommentForm(request.POST, request.FILES, instance=comment)
        
        if form.is_valid():
            form.save()
            return redirect('thread_detail', pk=comment.thread.pk)
    else:
        form = forms.CommentForm(instance=comment)

    return render(request, 'forum/edit_comment.html', {'form': form, 'comment': comment})

def delete_comment(request, pk):
    comment = get_object_or_404(models.Comment, pk=pk)

    if request.method == 'POST':
        comment.delete() 
        return redirect('thread_detail', pk=comment.thread.pk) 

    return render(request, 'forum/delete_comment.html', {'comment': comment})

def calendar(request):
    return render(request, 'group/calendar.html')

def create_event(request, day_month_year):
    day_month_year = datetime.strptime(day_month_year, "%Y-%m-%d").date()

    if request.method == 'POST':
        form = forms.EventForm(request.POST, initial={'day_month_year': day_month_year})
        if form.is_valid():
            event = form.save(commit=False)
            event.save()
        
            return redirect('calendar')
    else:
        form = forms.EventForm(initial={'day_month_year': day_month_year})

    return render(request, 'group/create_event.html', {'form': form, 'day_month_year': day_month_year})

def get_event_data(request, day_month_year):
    try:
        date_object = datetime.strptime(day_month_year, '%Y-%m-%d').date()
        events = models.Event.objects.filter(day_month_year=date_object)
        if events.exists():
            data = []
            for event in events:
                data.append({
                    'pk':event.pk,
                    'name': event.name,
                    'description': event.description,
                    'day_month_year': event.day_month_year.strftime('%Y-%m-%d'),
                    'time': event.time,
                })
            return JsonResponse(data, safe=False)  # safe=False позволяет вернуть список
        else:
            return JsonResponse({'error': 'Event not found'})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
  
def delete_event(request, pk):
    event = get_object_or_404(models.Event, pk=pk)

    if request.method == 'POST':
        event.delete() 
        return redirect('calendar') 

    return render(request, 'group/delete_event.html', {'event': event})

def edit_event(request, pk):
    event = get_object_or_404(models.Event, pk=pk)

    if request.method == 'POST':
        form = forms.EventForm(request.POST, instance=event)
        
        if form.is_valid():
            form.save()
            return redirect('calendar')
        else:
            print(form.errors)
    else:
        form = forms.EventForm(instance=event)

    return render(request, 'group/edit_event.html', {'form': form, 'event': event})

def events_for_month(request, year, month):
    events = models.Event.objects.filter(day_month_year__year=year)
    
    events_by_date = {}
    for event in events:
        event_date = event.day_month_year.strftime('%Y-%m-%d')
        if event_date not in events_by_date:
            events_by_date[event_date] = []
        events_by_date[event_date].append({
            'name': event.name,
            'description': event.description,
            'time': event.time.strftime('%H:%M')  
        })

    return JsonResponse(events_by_date)

def grades_list(request):
    grades = Grade.objects.all()
    return render(request, 'grades/grades_list.html', {'grades': grades})

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
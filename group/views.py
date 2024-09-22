from django.shortcuts import get_object_or_404, redirect, render
from group import models
from group.models import ForumThread
from django.contrib.auth.models import User
from django.contrib.auth import login
from group import forms
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.views.generic import DetailView, CreateView, DeleteView, UpdateView, View 

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

    
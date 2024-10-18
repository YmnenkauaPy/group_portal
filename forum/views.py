from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.views.generic import DetailView
from forum.models import ForumThread
from comment.forms import CommentForm
from forum.forms import ForumThreadForm
from django.core.paginator import Paginator 

def thread_list(request):
    threads = ForumThread.objects.all()
    

    paginator = Paginator(threads, 5)  
    page_number = request.GET.get('page') 
    page_obj = paginator.get_page(page_number) 

    return render(request, 'forum/thread_list.html', {'page_obj': page_obj})  


class ThreadDetailView(DetailView):
    model = ForumThread
    context_object_name = 'thread'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comment_form'] = CommentForm()
        return context
    
    def post(self, request, *args, **kwargs):
        comment_form = CommentForm(request.POST, request.FILES)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.author = request.user
            comment.thread = self.get_object()
            comment.save()

            return redirect('thread_detail', pk=comment.thread.pk)

@login_required
def thread_create(request):
    if request.method == 'POST':
        form = ForumThreadForm(request.POST)
        if form.is_valid():
            thread = form.save(commit=False)
            thread.author = request.user 
            thread.save()
            return redirect('thread_detail', pk=thread.pk)
    else:
        form = ForumThreadForm()
    
    return render(request, 'forum/thread_create.html', {'form': form})
    
@login_required
def thread_update(request, pk):
    thread = get_object_or_404(ForumThread, pk=pk)
    if request.method == 'POST':
        form = ForumThreadForm(request.POST, instance=thread)
        if form.is_valid():
            form.save()
            return redirect('thread_detail', pk=thread.pk)
    else:
        form = ForumThreadForm(instance=thread)
    return render(request, 'forum/thread_form.html', {'form': form})

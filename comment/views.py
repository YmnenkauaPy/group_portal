from django.shortcuts import get_object_or_404, redirect, render
from comment import models
from comment import forms

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
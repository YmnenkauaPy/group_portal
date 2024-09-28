from django.http import JsonResponse
from django.views import View
from django.shortcuts import get_object_or_404
from django.shortcuts import render
from like import models

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

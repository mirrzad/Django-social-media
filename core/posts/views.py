from django.shortcuts import render, redirect
from django.views import View
from .models import Post
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages


class PostDetailView(View):
    template_name = 'posts/post-detail.html'

    def get(self, request, post_id, post_slug):
        post = Post.objects.get(pk=post_id, slug=post_slug)
        return render(request, self.template_name, {'post': post})


class PostDeleteView(LoginRequiredMixin, View):
    def get(self, request, post_id):
        post = Post.objects.get(id=post_id)
        if request.user.id == post.user.id:
            post.delete()
            messages.success(request, 'Post Deleted Successfully', 'success')
        else:
            messages.error(request, 'You Can\'t Delete this post!', 'danger')
        return redirect('home:home-page')

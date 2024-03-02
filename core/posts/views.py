from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from .models import Post, Comment
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from .forms import PostCreateUpdateForm, CommentCreateForm, CommentReplyForm
from django.utils.text import slugify
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator


class PostDetailView(View):
    template_name = 'posts/post-detail.html'
    form_class = CommentCreateForm

    def setup(self, request, *args, **kwargs):
        self.post_instance = get_object_or_404(Post, pk=kwargs['post_id'], slug=kwargs['post_slug'])
        return super().setup(request, *args, **kwargs)

    def get(self, request, post_id, post_slug):
        comments = self.post_instance.pcomments.filter(is_reply=False)
        return render(request, self.template_name,
                      {
                        'post': self.post_instance,
                        'comments': comments,
                        'form': self.form_class,
                      })

    @method_decorator(login_required())
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.user = request.user
            new_comment.post = self.post_instance
            new_comment.save()
            messages.success(request, 'Thanks for your comment', 'success')
            return redirect('posts:post-detail', self.post_instance.id, self.post_instance.slug)


class PostDeleteView(LoginRequiredMixin, View):
    def get(self, request, post_id):
        post = get_object_or_404(Post, id=post_id)
        if request.user.id == post.user.id:
            post.delete()
            messages.success(request, 'Post Deleted Successfully', 'success')
        else:
            messages.error(request, 'You Can\'t Delete this post!', 'danger')
        return redirect('home:home-page')


class PostUpdateView(LoginRequiredMixin, View):
    form_class = PostCreateUpdateForm
    template_name = 'posts/post-update.html'

    def setup(self, request, *args, **kwargs):
        self.post_instance = get_object_or_404(Post, pk=kwargs['post_id'])
        return super().setup(request, *args, **kwargs)

    def dispatch(self, request, *args, **kwargs):
        post = self.post_instance
        if not request.user.id == post.user.id:
            messages.error(request, 'You Can\'t Update this post!', 'danger')
            return redirect('home:home-page')
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        post = self.post_instance
        form = self.form_class(instance=post)
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        post = self.post_instance
        form = self.form_class(request.POST, instance=post)
        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.slug = slugify(form.cleaned_data['body'][:30])
            new_post.save()
            messages.success(request, 'Post Updated Successfully', 'success')
            return redirect('posts:post-detail', new_post.id, new_post.slug)
        return redirect('posts:post-detail', post.id, post.slug)


class PostCreateView(LoginRequiredMixin, View):
    form_class = PostCreateUpdateForm
    template_name = 'posts/post-create.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.user = request.user
            new_post.slug = slugify(form.cleaned_data['body'][:30])
            new_post.save()
            messages.success(request, 'Post Created Successfully!', 'success')
            return redirect('posts:post-detail', new_post.id, new_post.slug)
        messages.error(request, 'Your inputs are Invalid!', 'danger')
        return redirect('account:profile-page', request.user.id)


class PostCommentReplyView(LoginRequiredMixin, View):
    form_class = CommentReplyForm
    template_name = 'posts/comment-reply.html'

    def get(self, request, post_id, comment_id):
        form = self.form_class
        return render(request, self.template_name, {'form': form})

    def post(self, request, post_id, comment_id):
        form = self.form_class(request.POST)
        post = get_object_or_404(Post, id=post_id)
        comment = get_object_or_404(Comment, id=comment_id)
        if form.is_valid():
            new_reply = form.save(commit=False)
            new_reply.user = request.user
            new_reply.post = post
            new_reply.reply = comment
            new_reply.is_reply = True
            new_reply.save()
            messages.success(request, 'Your reply submitted successfully!', 'success')
            return redirect('posts:post-detail', post.id, post.slug)


class PostReplyToReplyView(LoginRequiredMixin, View):
    form_class = CommentReplyForm
    template_name = 'posts/comment-reply.html'

    def get(self, request, post_id, comment_id, rep_id):
        form = self.form_class
        return render(request, self.template_name, {'form': form})

    def post(self, request, post_id, comment_id, rep_id):
        form = self.form_class(request.POST)
        post = get_object_or_404(Post, id=post_id)
        comment = get_object_or_404(Comment, id=comment_id)
        rep = get_object_or_404(Comment, id=rep_id)
        if form.is_valid():
            new_reply = form.save(commit=False)
            new_reply.user = request.user
            new_reply.post = post
            new_reply.reply = comment
            new_reply.reply_to_reply = rep
            new_reply.is_reply = True
            new_reply.save()
            messages.success(request, 'Your reply submitted successfully!', 'success')
            return redirect('posts:post-detail', post.id, post.slug)


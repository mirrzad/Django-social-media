from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    slug = models.SlugField(max_length=30)
    body = models.TextField(max_length=400)

    created_time = models.DateTimeField(auto_now=True)
    updated_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-created_time',)

    def __str__(self):
        return self.slug

    def get_absolute_url(self):
        return reverse('posts:post-detail', args=(self.pk, self.slug))


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ucomments')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='pcomments')
    reply = models.ForeignKey('self', on_delete=models.CASCADE, related_name='replies', null=True, blank=True)
    reply_to_reply = models.ForeignKey('self', on_delete=models.CASCADE, related_name='reps', null=True, blank=True)
    is_reply = models.BooleanField(default=False)
    body = models.TextField(max_length=300)
    created_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user}: {self.body[:20]}'

from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    slug = models.SlugField(max_length=30)
    body = models.TextField(max_length=400)

    created_time = models.DateTimeField(auto_now=True)
    updated_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.slug

    def get_absolute_url(self):
        return reverse('posts:post-detail', args=(self.pk, self.slug))

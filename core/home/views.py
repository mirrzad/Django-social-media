from django.shortcuts import render
from django.views import View
from posts.models import Post


class HomeView(View):
    template_name = 'home/index.html'

    def get(self, request):
        posts = Post.objects.all().order_by('-updated_time')
        return render(request, self.template_name, {'posts': posts})

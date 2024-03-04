from django.shortcuts import render
from django.views import View
from posts.models import Post
from posts.forms import SearchForm
from django.contrib import messages


class HomeView(View):
    template_name = 'home/index.html'
    form_class = SearchForm

    def get(self, request):
        posts = Post.objects.all()
        if request.GET.get('search'):
            posts = posts.filter(body__contains=request.GET['search'])
            if posts:
                return render(request, self.template_name, {'posts': posts, 'form': self.form_class})
            else:
                messages.error(request, 'Sorry! Your search doesn\'t exist.', 'danger')
        return render(request, self.template_name, {'posts': posts, 'form': self.form_class})

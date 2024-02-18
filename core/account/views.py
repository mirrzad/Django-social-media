from django.shortcuts import render, redirect
from django.views import View
from .forms import RegisterForm
from django.contrib.auth.models import User
from django.contrib import messages


class RegisterView(View):
    form_class = RegisterForm
    template_name = 'account/register.html'

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            User.objects.create(
                username=cd['username'],
                email=cd['email'],
                password=cd['password']
            )
            messages.success(request, 'Registration Done!', 'success')
            return redirect('home:home-page')
        return render(request, self.template_name, {'form': form})

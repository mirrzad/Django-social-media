from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import make_password
from django.contrib.auth import views as auth_views
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from .forms import RegisterForm, LoginForm, EditUserForm
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404
from .models import Relation


class UserRegisterView(View):
    form_class = RegisterForm
    template_name = 'account/register.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home:home-page')
        return super().dispatch(request, *args, **kwargs)

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
                password=make_password(cd['password'])
            )
            messages.success(request, 'Registration Done!', 'success')
            return redirect('home:home-page')
        return render(request, self.template_name, {'form': form})


class UserLoginView(View):
    form_class = LoginForm
    template_name = 'account/login.html'

    def setup(self, request, *args, **kwargs):
        self.next = request.GET.get('next')
        return super().setup(request, *args, **kwargs)

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home:home-page')
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request, username=cd['username'], password=cd['password'])
            if user is not None:
                login(request, user)
                messages.success(request, 'You are logged in successfully', 'success')
                if self.next:
                    return redirect(self.next)
                return redirect('home:home-page')
            else:
                messages.error(request, 'Username or password is wrong!', 'warning')
        return render(request, self.template_name, {'form': form})


class UserLogoutView(LoginRequiredMixin, View):
    def get(self, request):
        logout(request)
        messages.success(request, 'You are logged out successfully', 'success')
        return redirect('home:home-page')


class UserProfileView(LoginRequiredMixin, View):
    template_name = 'account/profile.html'

    def get(self, request, user_id):
        is_following = False
        try:
            user = User.objects.prefetch_related('posts').get(pk=user_id)
            if Relation.objects.filter(from_user=request.user, to_user=user).exists():
                is_following = True
            return render(request, self.template_name, {'user': user, 'is_following': is_following})
        except User.DoesNotExist:
            raise Http404


class UserPasswordResetView(auth_views.PasswordResetView):
    template_name = 'account/password_reset_form.html'
    success_url = reverse_lazy('account:password-reset-done')
    email_template_name = 'account/password_reset_email.html'


class UserPasswordResetDoneView(auth_views.PasswordResetDoneView):
    template_name = 'account/password_reset_done.html'


class UserPasswordResetConfirmView(auth_views.PasswordResetConfirmView):
    template_name = 'account/password_reset_confirm.html'
    success_url = reverse_lazy('account:password-reset-complete')


class UserPasswordResetCompleteView(auth_views.PasswordResetCompleteView):
    template_name = 'account/password_reset_complete.html'


class UserFollowView(LoginRequiredMixin, View):

    def dispatch(self, request, *args, **kwargs):
        if request.user.id == kwargs['user_id']:
            messages.error(request, 'You can\'t follow yourself!', 'danger')
            return redirect('account:profile-page', user_id=kwargs['user_id'])
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, user_id):
        user = User.objects.get(id=user_id)
        if Relation.objects.filter(from_user=request.user, to_user=user).exists():
            messages.error(request, 'You already follow this account!', 'danger')
        else:
            Relation(from_user=request.user, to_user=user).save()
            messages.success(request, 'You are following this account!', 'success')
        return redirect('account:profile-page', user_id=user.id)


class UserUnfollowView(LoginRequiredMixin, View):

    def dispatch(self, request, *args, **kwargs):
        if request.user.id == kwargs['user_id']:
            messages.error(request, 'You can\'t unfollow yourself!', 'danger')
            return redirect('account:profile-page', user_id=kwargs['user_id'])
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, user_id):
        user = User.objects.get(id=user_id)
        relation = Relation.objects.filter(from_user=request.user, to_user=user)
        if relation:
            relation.delete()
            messages.success(request, 'You  unfollowed the account successfully!', 'success')
        else:
            messages.error(request, 'You don\'t follow this account!', 'danger')
        return redirect('account:profile-page', user_id=user.id)


class EditUserProfile(LoginRequiredMixin, View):
    form_class = EditUserForm
    template_name = 'account/edit-user-profile.html'

    def get(self, request):
        form = self.form_class(instance=request.user.profile, initial={'email': request.user.email})
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST, instance=request.user.profile)
        if form.is_valid():
            form.save()
            request.user.email = form.cleaned_data['email']
            request.user.save()
            messages.success(request, 'Your profile edited successfully!', 'success')
        return redirect('account:profile-page', request.user.id)

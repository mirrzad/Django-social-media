from django.urls import path
from . import views

app_name = 'account'

urlpatterns = [
    path('register/', views.UserRegisterView.as_view(), name='register-page'),
    path('login/', views.UserLoginView.as_view(), name='login-page'),
    path('logout/', views.UserLogoutView.as_view(), name='logout-page'),
    path('profile/<int:user_id>/', views.UserProfileView.as_view(), name='profile-page'),
    path('password_reset/', views.UserPasswordResetView.as_view(), name='password-reset'),
    path('password_reset_done/', views.UserPasswordResetDoneView.as_view(), name='password-reset-done'),
    path('password_reset_confirm/<uidb64>/<token>/',
         views.UserPasswordResetConfirmView.as_view(), name='password-reset-confirm'),
    path('password_reset_complete/', views.UserPasswordResetCompleteView.as_view(), name='password-reset-complete'),
    path('follow/<int:user_id>/', views.UserFollowView.as_view(), name='user-follow'),
    path('unfollow/<int:user_id>/', views.UserUnfollowView.as_view(), name='user-unfollow'),
]

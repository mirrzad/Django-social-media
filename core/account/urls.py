from django.urls import path
from . import views

app_name = 'account'

urlpatterns = [
    path('register/', views.UserRegisterView.as_view(), name='register-page'),
    path('login/', views.UserLoginView.as_view(), name='login-page'),
    path('logout/', views.UserLogoutView.as_view(), name='logout-page'),
    path('profile/<int:user_id>/', views.UserProfileView.as_view(), name='profile-page'),
]

from django.urls import path
from . import views

app_name = 'posts'

urlpatterns = [
    path('<int:post_id>/<slug:post_slug>/', views.PostDetailView.as_view(), name='post-detail'),
    path('delete/<int:post_id>', views.PostDeleteView.as_view(), name='post-delete'),
]

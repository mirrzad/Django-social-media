from django.urls import path
from . import views

app_name = 'posts'

urlpatterns = [
    path('<int:post_id>/<slug:post_slug>/', views.PostDetailView.as_view(), name='post-detail'),
    path('delete/<int:post_id>', views.PostDeleteView.as_view(), name='post-delete'),
    path('update/<int:post_id>', views.PostUpdateView.as_view(), name='post-update'),
    path('create/', views.PostCreateView.as_view(), name='post-create'),
    path('comment-reply/<int:post_id>/<int:comment_id>/', views.PostCommentReplyView.as_view(), name='comment-reply'),
    path('reply-reply/<int:post_id>/<int:comment_id>/<int:rep_id>/',
         views.PostReplyToReplyView.as_view(), name='reply-reply'),
]

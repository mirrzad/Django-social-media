from django.contrib import admin
from .models import Post, Comment, Like


class PostAdmin(admin.ModelAdmin):
    list_display = ('slug', 'user', 'updated_time')
    list_filter = ('slug', 'user', 'updated_time')
    search_fields = ('slug',)
    prepopulated_fields = {'slug': ('body',)}


class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'post', 'created_time', 'is_reply')
    raw_id_fields = ('user', 'post', 'reply')


class LikeAdmin(admin.ModelAdmin):
    list_display = ('user', 'post')
    raw_id_fields = ('user', 'post')


admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Like, LikeAdmin)

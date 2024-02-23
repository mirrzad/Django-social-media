from django.contrib import admin
from .models import Post


class PostAdmin(admin.ModelAdmin):
    list_display = ('slug', 'user', 'updated_time')
    list_filter = ('slug', 'user', 'updated_time')
    search_fields = ('slug',)
    prepopulated_fields = {'slug': ('body',)}


admin.site.register(Post, PostAdmin)

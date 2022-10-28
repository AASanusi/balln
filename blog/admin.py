from django.contrib import admin
from .models import Post
from django_summernote.admin import SummernoteModelAdmin


@admin.register(Post)
class PostAdmin(SummernoteModelAdmin):

    list_display = ('title', 'slug', 'status', 'date_added')
    prepopulated_fields = {'slug': ('title',)}
    list_filter = ('status', 'date_added')
    summernote_fields = ('body')
    search_fields = ('title', 'body')

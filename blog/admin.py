from django.contrib import admin
from .models import Post, Comment
from django_summernote.admin import SummernoteModelAdmin


@admin.register(Post)
class PostAdmin(SummernoteModelAdmin):

    list_display = ('title', 'slug', 'status', 'date_added')
    prepopulated_fields = {'slug': ('title',)}
    list_filter = ('status', 'date_added')
    summernote_fields = ('body')
    search_fields = ('title', 'body')


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):

    list_display = ('name', 'body', 'post', 'date_added', 'approved')
    list_filter = ('approved', 'date_added')
    search_fields = ('name', 'email', 'body')
    actions = ['approve_comments']

    def approve_comments(self, request, queryset):
        queryset.update(approved=True)

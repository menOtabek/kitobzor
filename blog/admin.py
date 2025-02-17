from django.contrib import admin
from .models import Post, PostComment

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('user', 'book_name', 'book_author')
    list_filter = ('user', 'book_name')
    search_fields = ('user', 'book_name')


@admin.register(PostComment)
class PostCommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'post', 'comment')
    list_filter = ('user', 'post')
    search_fields = ('user', 'post')

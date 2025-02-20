from django.contrib import admin
from sharing.models import Book, BookComment


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'name', 'author', 'publication_year', 'is_active')
    list_filter = ('id', 'name', 'author')
    search_fields = ('id', 'name', 'author', 'user__telegram_id')


@admin.register(BookComment)
class BookCommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'book', 'comment', 'is_banned')
    list_filter = ('id', 'user', 'book')
    search_fields = ('id', 'user__telegram_id', 'book')

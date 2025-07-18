from django.contrib import admin
from sharing.models import Book, BookComment, Category


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'author', 'publication_year', 'is_active')
    list_filter = ('id', 'name', 'author')
    search_fields = ('id', 'name', 'author')


@admin.register(BookComment)
class BookCommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'book', 'comment', 'is_banned')
    list_filter = ('id', 'user', 'book')
    search_fields = ('id', 'user__telegram_id', 'book')

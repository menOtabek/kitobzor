from django.contrib import admin
from .models import User

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('telegram_id', 'is_active', 'role')
    list_display_links = ('telegram_id', 'role')
    readonly_fields = ('telegram_id', 'role')

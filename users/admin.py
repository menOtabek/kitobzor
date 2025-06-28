from django.contrib import admin
from .models import User, Otp

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('telegram_id', 'is_active', 'role')
    list_display_links = ('telegram_id', 'role')


@admin.register(Otp)
class OtpAdmin(admin.ModelAdmin):
    list_display = ('user', 'otp_code')
    list_display_links = ('user', 'otp_code')

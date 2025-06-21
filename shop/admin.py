from django.contrib import admin
from .models import Shop, ShopStuff

@admin.register(Shop)
class ShopAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'location_text', 'is_active')
    list_display_links = ('id', 'name')
    search_fields = ('name',)
    list_filter = ('is_active', 'region', 'district')


@admin.register(ShopStuff)
class ShopStuffAdmin(admin.ModelAdmin):
    list_display = ('id', 'is_active')
    list_display_links = ('id', 'is_active')
    list_filter = ('is_active',)

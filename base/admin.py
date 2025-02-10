from django.contrib import admin
from .models import Region, District, DefaultBookOffer

@admin.register(Region)
class RegionAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')
    search_fields = ('name',)


@admin.register(District)
class DistrictAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'region')
    list_display_links = ('id', 'name')
    search_fields = ('name',)


@admin.register(DefaultBookOffer)
class DefaultBookOfferAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'book_name')
    list_display_links = ('id', 'book_name')
    search_fields = ('book_name', 'book_author')

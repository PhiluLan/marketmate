from django.contrib import admin
from .models import Website

@admin.register(Website)
class WebsiteAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'url', 'user', 'created_at')
    list_filter  = ('user', 'created_at')
    search_fields = ('name', 'url')

from django.contrib import admin
from .models import Content

@admin.register(Content)
class ContentAdmin(admin.ModelAdmin):
    list_display = ('id','title','ad_account_id')
    search_fields = ('title',)

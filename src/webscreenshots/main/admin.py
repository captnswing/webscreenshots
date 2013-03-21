from django.contrib import admin
from models import WebSite

class WebSiteOptions(admin.ModelAdmin):
    ordering = ['category', 'title']
    save_on_top = True
    list_display = ['title', 'category']

admin.site.register(WebSite, WebSiteOptions)

from django.contrib import admin
from main.models import WebSite

class WebSiteOptions(admin.ModelAdmin):
    ordering = ['url']
    save_on_top = True

admin.site.register(WebSite, WebSiteOptions)

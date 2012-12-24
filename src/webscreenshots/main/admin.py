from django.contrib import admin
from models import WebSite

class WebSiteOptions(admin.ModelAdmin):
    ordering = ['url']
    save_on_top = True

admin.site.register(WebSite, WebSiteOptions)

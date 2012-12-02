#-*- coding: utf-8 -*-
from django.db import models

class WebSite(models.Model):
    # TODO: validate entered URL, check that site exists
    url = models.CharField('URL för webbsidan', max_length=250)

    def __unicode__(self):
        return self.url.lstrip('http://')

    class Meta:
        verbose_name = "webbsida"
        verbose_name_plural = "webbsidor"

#-*- coding: utf-8 -*-
from django.db import models

class WebSite(models.Model):
    # TODO: validate entered URL, check that site exists
    url = models.CharField('URL för webbsidan', max_length=250)

    def __unicode__(self):
        return self.url.lstrip('http://').lstrip('www.').rstrip('/')

    def save(self, *args, **kwargs):
        self.url = self.url.rstrip('/')
        if not "http://" in self.url:
            self.url = "http://" + self.url
        super(WebSite, self).save(*args, **kwargs) # Call the "real" save() method.

    class Meta:
        verbose_name = "webbsida"
        verbose_name_plural = "webbsidor"

#-*- coding: utf-8 -*-
from django.db import models


class WebSite(models.Model):
    # TODO: validate entered URL, check that site exists
    url = models.CharField('URL för webbsidan', max_length=250)
    # title = models.CharField('Titel för webbsidan', max_length=250, blank=True)

    def __unicode__(self):
        return self.url.replace('http://', '').replace('www.', '').rstrip('/')

    def save(self, *args, **kwargs):
        self.url = self.url.replace('http://', '').replace('www.', '').rstrip('/')
        self.url = "http://" + self.url
        super(WebSite, self).save(*args, **kwargs) # Call the "real" save() method.

    class Meta:
        ordering = ["url"]
        verbose_name = "webbsida"
        verbose_name_plural = "webbsidor"

#-*- coding: utf-8 -*-
from urlparse import urlsplit
from django.db import models

CATEGORY_CHOICES = (
    ('1', 'International'),
    ('2', 'Riks'),
    ('3', 'Regionala'),
)


class WebSite(models.Model):
    # TODO: validate entered URL, check that site exists
    url = models.CharField('URL för webbsidan', max_length=250)
    title = models.CharField('Titel för webbsidan', max_length=250, blank=True)
    category = models.CharField(choices=CATEGORY_CHOICES, max_length=3, blank=True)

    def __unicode__(self):
        return self.title

    @property
    def canonicalurl(self):
        parsed = urlsplit(self.url)
        canonicalurl = parsed.netloc.lstrip('www.')
        urlpath = parsed.path.strip('/')
        if urlpath:
            canonicalurl += "|" + urlpath.replace('/', '|')
        return canonicalurl

    def save(self, *args, **kwargs):
        self.url = self.url.replace('http://', '').replace('www.', '').rstrip('/')
        self.url = "http://" + self.url.strip()
        super(WebSite, self).save(*args, **kwargs) # Call the "real" save() method.

    class Meta:
        ordering = ["category", "title"]
        verbose_name = "webbsida"
        verbose_name_plural = "webbsidor"

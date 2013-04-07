#-*- coding: utf-8 -*-
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

    def save(self, *args, **kwargs):
        self.url = self.url.replace('http://', '').replace('www.', '').rstrip('/')
        self.url = "http://" + self.url.strip()
        super(WebSite, self).save(*args, **kwargs) # Call the "real" save() method.

    class Meta:
        ordering = ["category", "title"]
        verbose_name = "webbsida"
        verbose_name_plural = "webbsidor"

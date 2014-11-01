#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os

os.environ["DJANGO_SETTINGS_MODULE"] = 'webscreenshots.settings.frank'
from webscreenshots.main.models import WebSite
import csv

reg = csv.reader(open('reg.csv', 'r'), delimiter=',')
for row in reg:
    WebSite.objects.get_or_create(title=row[1], url=row[2])

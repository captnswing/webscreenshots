#-*- coding: utf-8 -*-
import os
os.environ["DJANGO_SETTINGS_MODULE"] = "settings"
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from boto.s3.connection import S3Connection
import datetime


def get_sites_for_day(selected_day):
    conn = S3Connection()
    bucket = conn.get_bucket('svti-webscreenshots')
    selected_day = selected_day.strftime("%Y/%m/%d")
    keys = bucket.get_all_keys(prefix=selected_day + "/", delimiter="/")
    sites = [ key.name.lstrip(selected_day).rstrip("/").replace('|', '/') for key in keys ]
    return sites


def home(request, pubdate=None):
    if not pubdate:
        d = datetime.datetime.today()
    else:
        y, m, d = pubdate.split('-')
        d = datetime.datetime(int(y), int(m), int(d))
    return render_to_response('home.html', {
        'selected_day': d.ctime()
    }, context_instance=RequestContext(request))

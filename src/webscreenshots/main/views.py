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
    sites = [key.name.lstrip(selected_day).rstrip("/").replace('|', '/') for key in keys]
    return sites


# from http://stackoverflow.com/a/312464/41404
def chunks(l, n):
    """ Yield successive n-sized chunks from l.
    """
    for i in xrange(0, len(l), n):
        yield l[i:i + n]


def home(request, pubdate=None):
    if not pubdate:
        d = datetime.datetime.today()
    else:
        y, m, d = pubdate.split('-')
        d = datetime.datetime(int(y), int(m), int(d))
    keyname = "sites_%s" % d.strftime("%Y-%m-%d")
    if keyname in request.session:
        sitesforday = request.session[keyname]
    else:
        sitesforday = get_sites_for_day(d)
        request.session[keyname] = sitesforday
    return render_to_response('home.html', {
        'sitechunks': chunks(sitesforday, 7),
        'selected_day': d.ctime()
    }, context_instance=RequestContext(request))

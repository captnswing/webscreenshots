#-*- coding: utf-8 -*-
import os
from django.http import HttpResponseRedirect
import json
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
    thumbwidth = request.GET.get("thumbwidth", 220)
    lens = request.GET.get("lens", "on")

    firstdataday = datetime.datetime(2013, 1, 3)
    today = datetime.datetime.today()
    if not pubdate:
        d = today
    else:
        y, m, d = pubdate.split('-')
        d = datetime.datetime(int(y), int(m), int(d))
        # if specified date is todays'
        if d.timetuple()[:3] == today.timetuple()[:3]:
            d = today
    if d < firstdataday:
        return HttpResponseRedirect('/%s' % firstdataday.strftime("%Y-%m-%d"))
    if d > today:
        return HttpResponseRedirect('/%s' % today.strftime("%Y-%m-%d"))

    keyname = "sites_%s" % d.strftime("%Y-%m-%d")
    if keyname in request.session:
        sitesforday = request.session[keyname]
    else:
        sitesforday = get_sites_for_day(d)
        request.session[keyname] = sitesforday

    sites = request.GET.get("sites", [])
    if not sites:
        sites = ["aftonbladet.se", "expressen.se", "svt.se/nyheter", "svd.se", "dn.se"]
    else:
        sites = sites.split(',')

    wrongsites = [ s for s in sites if s not in sitesforday ] or None
    sites = [ s for s in sites if s in sitesforday ]

    offhours = [23, 0, 1, 2, 3, 4, 5, 6]

    return render_to_response('home.html', {
        'thumbwidth': thumbwidth,
        'loupe': lens,
        'offhours': json.dumps(offhours),
        'first_data_day': firstdataday.ctime(),
        'selected_day': d.ctime(),
        'selected_sites': sites,
        'selected_sites_json': json.dumps(sites),
        'wrongsites_json': json.dumps(wrongsites),
        'allsites': chunks(sitesforday, 8),
    }, context_instance=RequestContext(request))

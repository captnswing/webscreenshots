#-*- coding: utf-8 -*-
import os
os.environ["DJANGO_SETTINGS_MODULE"] = "settings"
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.http import HttpResponse
import json
from boto.s3.connection import S3Connection
import datetime
from collections import defaultdict


domain = "http://d2np6cnk6s6ggj.cloudfront.net"


def get_sites_for_day(bucket, selected_day):
    selected_day = selected_day.strftime("%Y/%m/%d")
    keys = bucket.get_all_keys(prefix=selected_day + "/", delimiter="/")
    sites = [ key.name.lstrip(selected_day).rstrip("/").replace('|', '/') for key in keys ]
    return sites


def get_images_for_day_and_site(selected_day, selected_site):
    conn = S3Connection()
    bucket = conn.get_bucket('svti-webscreenshots')
    if isinstance(selected_day, datetime.datetime) or isinstance(selected_day, datetime.date):
        selected_day = selected_day.strftime("%Y/%m/%d")
    imagekeys = bucket.get_all_keys(prefix=selected_day + "/" + selected_site + "/")
#    imagekeys = [ ik.name for ik in imagekeys if "-thumb.jpg" in ik.name ]
    imagekeys = [ ik.name for ik in imagekeys if ".00" in ik.name  ]
    return imagekeys


def get_hour_thumbs(selected_site, selected_day):
    imagekeys = get_images_for_day_and_site(selected_site, selected_day)
    if not imagekeys:
        return {}
    hours = sorted(list(set([ k.split('/')[-1].split('-')[0].split('.')[0] for k in imagekeys ])))
    hourthumbs = {}
    url_templ = domain + "/".join(imagekeys[0].split('/')[:-1])
    url_templ += "/%s.00-thumb.jpg"
    for h in hours:
        hourthumbs[int(h)] = url_templ % h
    return hourthumbs


def siteday(request, pubdate):
    sites = request.POST.getlist('sites[]')
    y, m, d = pubdate.split('-')
    d = datetime.datetime(int(y), int(m), int(d))
    d = d.replace(microsecond=0).replace(second=0).replace(minute=0)
    dhours = [ d.replace(hour=i) for i in range(24) ]
#    result_data = defaultdict(list)
    result_data = []
    for site in sites:
        baseurl = domain + "/" + pubdate.replace('-', '/') + "/" + site.replace('/', '|') + "/"
        siteurls = [ baseurl + d.strftime("%H.%M") for d in dhours ]
        result_data.append(siteurls)
#        for k, v in zip(dhours, siteurls):
#            result_data[k.isoformat()].append(v)
    dthandler = lambda obj: obj.isoformat() if isinstance(obj, datetime.datetime) else None
    return HttpResponse(json.dumps(zip(*result_data), default=dthandler))#, mimetype="application/json")


def home(request, pubdate=None):
    if not pubdate:
        d = datetime.datetime.today()
    else:
        y, m, d = pubdate.split('-')
        d = datetime.datetime(int(y), int(m), int(d))
    return render_to_response('home.html', {
        'selected_day': d.ctime()
    }, context_instance=RequestContext(request))


if __name__ == '__main__':
    td = datetime.datetime.today()
    td = td.replace(microsecond=0).replace(second=0).replace(minute=0)
    for i in range(24):
        print td.replace(hour=i).strftime("%H.%M")

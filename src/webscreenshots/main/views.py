#-*- coding: utf-8 -*-
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from boto.s3.connection import S3Connection
import datetime


domain = "http://d2np6cnk6s6ggj.cloudfront.net/"


def get_sites_for_day(selected_day):
    conn = S3Connection()
    bucket = conn.get_bucket('svti-webscreenshots')
    selected_day = selected_day.strftime("%Y/%m/%d")
    keys = bucket.get_all_keys(prefix=selected_day + "/", delimiter="/")
    sites = [ key.name.lstrip(selected_day).rstrip("/").replace('|', '/') for key in keys ]
    return sites


def get_images_for_day_and_site(selected_site, selected_day):
    conn = S3Connection()
    bucket = conn.get_bucket('svti-webscreenshots')
    if isinstance(selected_day, datetime.datetime) or isinstance(selected_day, datetime.date):
        selected_day = selected_day.strftime("%Y/%m/%d")
#    selected_day = todaystr
    imagekeys = bucket.get_all_keys(prefix=selected_day + "/" + selected_site + "/")
    imagekeys = [ ik.name for ik in imagekeys if "-thumb.jpg" in ik.name ]
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


def siteday(request, pubdate, site):
    urls = get_images_for_day_and_site(pubdate.replace('-', '/'), site)
#    json.dumps(response_data), mimetype="application/json")
    td = datetime.datetime.today()
    td = td.replace(microsecond=0).replace(second=0).replace(minute=0)
    currenthour = td
    ht = get_hour_thumbs("svt.se", datetime.date.today() + datetime.timedelta(days=0))
    hourthumbs = []
    for i in range(24):
        ht_dict = {'hour': td.replace(hour=i), 'url': ht.get(i, None)}
        hourthumbs.append(ht_dict)
    return render_to_response('contentflow.html', {
        'urls': urls,
        'hourthumbs': hourthumbs,
        'currenthour': currenthour
    }, context_instance=RequestContext(request))


def home(request):
    conn = S3Connection()
    bucket = conn.get_bucket('svti-webscreenshots')
    domain = bucket.get_website_endpoint()
    sites = get_sites_for_day(datetime.date.today())
    return render_to_response('contentflow.html', {
        'sites': sites,
        'domain': domain,
    }, context_instance=RequestContext(request))


if __name__ == '__main__':
    td = datetime.datetime.today()
    td = td.replace(microsecond=0).replace(second=0).replace(minute=0)
    for i in range(24):
        print td.replace(hour=i).strftime("%H.%M")

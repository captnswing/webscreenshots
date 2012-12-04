#-*- coding: utf-8 -*-
from django.shortcuts import render_to_response
from django.template.context import RequestContext
import os
from boto.s3.connection import S3Connection
from boto.s3.key import Key
import sys
import datetime


domain = "http://d2np6cnk6s6ggj.cloudfront.net/"
AWS_ACCESS_KEY = os.environ["AWS_ACCESS_KEY"]
AWS_SECRET_KEY = os.environ["AWS_SECRET_KEY"]


def get_sites_for_day(selected_day):
    conn = S3Connection(AWS_ACCESS_KEY, AWS_SECRET_KEY)
    bucket = conn.get_bucket('svti-webscreenshots')
    selected_day = selected_day.strftime("%Y/%m/%d")
    keys = bucket.get_all_keys(prefix=selected_day + "/", delimiter="/")
    sites = [ key.name.lstrip(selected_day).rstrip("/").replace('|', '/') for key in keys ]
    return sites


def home(request):
    conn = S3Connection(AWS_ACCESS_KEY, AWS_SECRET_KEY)
    bucket = conn.get_bucket('svti-webscreenshots')
    domain = bucket.get_website_endpoint()
    sites = get_sites_for_day(datetime.date.today())
    return render_to_response('test.html', {'sites': sites}, context_instance=RequestContext(request))


if __name__ == '__main__':
    print get_sites_for_day(datetime.date.today())

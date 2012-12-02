#-*- coding: utf-8 -*-
from django.shortcuts import render_to_response
from django.template.context import RequestContext
import os
from boto.s3.connection import S3Connection
from boto.s3.key import Key
import sys

domain = "http://d2np6cnk6s6ggj.cloudfront.net/"

def home(request):
    AWS_ACCESS_KEY = os.environ["AWS_ACCESS_KEY"]
    AWS_SECRET_KEY = os.environ["AWS_SECRET_KEY"]
    conn = S3Connection(AWS_ACCESS_KEY, AWS_SECRET_KEY)
    bucket = conn.get_bucket('svti-webscreenshots')
    domain = bucket.get_website_endpoint()
    rs = bucket.list("2012/12/02/tv4")
    fns = [ key.name.lstrip("2012/12/02") for key in bucket.list("2012/12/02/tv4") ]
    d = {}
    for fn in fns:
        parts = fn.split('-')
        timestamp = parts[-2]
        site = "/".join(parts[:-2])
        print site
        print timestamp

    key = list(rs)[0]
    return render_to_response('test.html', {'rs': rs}, context_instance=RequestContext(request))

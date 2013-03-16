#!/usr/bin/env python
#-*- coding: utf-8 -*-
from boto.s3.connection import S3Connection
import os
import datetime


if __name__ == '__main__':
    sitetoremove = "di.se"
    AWS_ACCESS_KEY = os.environ["AWS_ACCESS_KEY"]
    AWS_SECRET_KEY = os.environ["AWS_SECRET_KEY"]
    conn = S3Connection(AWS_ACCESS_KEY, AWS_SECRET_KEY)
    bucket = conn.get_bucket("svti-webscreenshots")
    d = datetime.datetime(2013, 1, 4)
    delta = datetime.timedelta(days=1)
    while d <= datetime.datetime.today():
        path = "%s/%s" % (d.strftime("%Y/%m/%d"), sitetoremove)
        print path
        bucketListResultSet = bucket.list(prefix=path)
        result = bucket.delete_keys([key.name for key in bucketListResultSet])
        d += delta

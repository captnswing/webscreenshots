#!/usr/bin/env python
#-*- coding: utf-8 -*-
from webscreenshots.celeryapp import celery
from boto import connect_s3
from django.conf import settings
import datetime
from webscreenshots.main.utils import calculate_expexted_times


def daterange(start_date, end_date):
    for n in range(int((end_date - start_date).days)):
        yield start_date + datetime.timedelta(n)


def get_expected_files():
    extensions = ('.jpg', '-thumb.jpg', '-top.jpg')
    expected_times = calculate_expexted_times()
    expected_files = ["{0}{1}".format(et, ext) for et in expected_times for ext in extensions]
    return set(expected_files)


def get_sites_for_day(selected_day):
    conn = connect_s3(settings.AWS_ACCESS_KEY, settings.AWS_SECRET_KEY)
    bucket = conn.get_bucket(settings.S3_BUCKET_NAME)
    selected_day = selected_day.strftime("%Y/%m/%d")
    keys = bucket.get_all_keys(prefix=selected_day + "/", delimiter="/")
    sites = [key.name.rstrip("/") for key in keys]
    return sites


def get_site_files(site):
    conn = connect_s3(settings.AWS_ACCESS_KEY, settings.AWS_SECRET_KEY)
    bucket = conn.get_bucket(settings.S3_BUCKET_NAME)
    keys = bucket.get_all_keys(prefix=site + "/", delimiter="/")
    sitefiles = [key.name.split('/')[-1] for key in keys]
    print sitefiles
    return set(sitefiles)


def main():
    ef = get_expected_files()
    print len(ef)
    for single_date in daterange(datetime.datetime(2013, 4, 1), datetime.datetime.today()):
        sites = get_sites_for_day(single_date)
        for single_site in sites:
            sf = get_site_files(single_site)
            missing_files = ef - sf
            strange_files = sf - ef
            print strange_files
            selected_day = single_date.strftime("%Y/%m/%d")
            site_url = single_site.replace(selected_day, '').replace('|', '/').strip('/')
            print selected_day, site_url, len(missing_files)


if __name__ == '__main__':
    main()

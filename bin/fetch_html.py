#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys
import requests
import hashlib
import django
import multiprocessing
from urlparse import urlparse
from pyquery import PyQuery as pq
from lxml.html import tostring as html2str
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "webscreenshots.settings.frank")
django.setup()
from webscreenshots.main.models import WebSite
from webscreenshots.absolutism import make_all_absolute


def get_html(url):
    """get html and parse it into DOM object"""
    print 'get: {}'.format(url)
    r = requests.get(url)
    cleanhtml = r.text.replace("""<?xml version="1.0" encoding="UTF-8"?>""", "")
    d = pq(cleanhtml, parser='html')
    return d


def write_html(d, html_filename):
    """write html to file"""
    html = open('data/{}'.format(html_filename), 'wb')
    # from http://stackoverflow.com/a/13444679/41404
    html.write(html2str(d.root))
    print 'wrote: {}'.format(html_filename)
    html.close()


def workon(website):
    """thread worker function"""
    # base variables
    canonical_url = website.url.replace('http://', '').replace('www.', '')
    hashed_url = hashlib.md5(canonical_url).hexdigest()
    base_url = "://".join(urlparse(website.url)[:2])

    # fetch html
    d = get_html(website.url)

    # make absolute
    d = make_all_absolute(d, base_url)

    # write html to file
    html_filename = '{}.html'.format(canonical_url.replace('/', '_'))
    write_html(d, html_filename)
    return


def main():
    jobs = []
    for ws in WebSite.objects.all():
        # if not ws.title == "SR P4 Blekinge":
        #     continue
        p = multiprocessing.Process(target=workon, args=(ws,))
        jobs.append(p)
        p.start()


if __name__ == '__main__':
    main()

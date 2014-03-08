#!/usr/bin/env python
#-*- coding: utf-8 -*-
from main.models import WebSite
import hashlib
import multiprocessing
import codecs
from pyquery import PyQuery as pq
import requests
from urlparse import urlparse


def save_html(website):
    """thread worker function"""

    # base variables
    canonical_url = website.url.replace('http://', '').replace('www.', '')
    hashed_url = hashlib.md5(canonical_url).hexdigest()
    base_url = "://".join(urlparse(website.url)[:2])
    print 'get:   {}'.format(website.url)

    # fetch html
    try:
        d = pq(website.url)
    except ValueError:
        r = requests.get(website.url)
        cleanhtml = r.text.replace("""<?xml version="1.0" encoding="UTF-8"?>""", "")
        d = pq(cleanhtml)

    # relative -> absolute
    d('head').append('<base href="{}"'.format(base_url))
    # finds all script tags that have a src attribute whose value starts with '/'
    for fixs in d('script[src^="/"]'):
        absolutepath = base_url + pq(fixs).attr['src']
        pq(fixs).attr['src'] = absolutepath
    # finds all link tags that have a href attribute whose value starts with '/'
    for fixl in d('link[href^="/"]'):
        absolutepath = base_url + pq(fixl).attr['href']
        pq(fixl).attr['href'] = absolutepath
        print absolutepath

    # write html to file
    html_filename = '{}.html'.format(canonical_url.replace('/', '_'))
    html = codecs.open('data/{}'.format(html_filename), 'wb', 'utf-8')
    print 'write: {}'.format(html_filename)
    html.write(d.html())
    html.close()
    return


def main():
    jobs = []
    for ws in WebSite.objects.all():
        if not ws.url == "http://sverigesradio.se/sida/default.aspx?programid=125":
            continue
        p = multiprocessing.Process(target=save_html, args=(ws,))
        jobs.append(p)
        p.start()


if __name__ == '__main__':
    main()

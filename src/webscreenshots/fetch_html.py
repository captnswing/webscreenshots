#!/usr/bin/env python
#-*- coding: utf-8 -*-
from main.models import WebSite
import hashlib
import multiprocessing
import codecs
from pyquery import PyQuery as pq
import requests
from urlparse import urlparse


def download_css(filename):
    d = pq(open(filename).read())
    for fixl in d('link[href^="/"]'):
        print pq(fixl).attr['href']


def add_base_tag(d, base_url):
    # add (or update) base tag!
    if d('base'):
        d('base').attr['href'] = base_url
    else:
        d('head').append('<base href="{}"'.format(base_url))
    return d

def make_absolute(d, base_url):

    # finds all script tags that have a src attribute whose value starts with '/'
    for fixs in d('script[src^="/"]'):
        # prepend base_url to the src value
        absolutepath = base_url + pq(fixs).attr['src']
        pq(fixs).attr['src'] = absolutepath

    # from http://pythonhosted.org/pyquery/tips.html
    d.make_links_absolute(base_url=base_url)

    # finds all link tags that have a href attribute whose value starts with '/'
    # for fixl in d('link[href^="/"]'):
    #     absolutepath = base_url + pq(fixl).attr['href']
    #     pq(fixl).attr['href'] = absolutepath
    #     print absolutepath
    return d


def write_html(d, html_filename):
    """write html to file"""
    html = codecs.open('data/{}'.format(html_filename), 'wb', 'utf-8')
    print 'write: {}'.format(html_filename)
    html.write(d.outer_html())
    html.close()


def save_html(website):
    """thread worker function"""

    # base variables
    canonical_url = website.url.replace('http://', '').replace('www.', '')
    hashed_url = hashlib.md5(canonical_url).hexdigest()
    base_url = "://".join(urlparse(website.url)[:2])
    print 'get:   {}'.format(website.url)

    # fetch html
    try:
        d = pq(website.url, parser='html')
    except ValueError:
        r = requests.get(website.url)
        cleanhtml = r.text.replace("""<?xml version="1.0" encoding="UTF-8"?>""", "")
        d = pq(cleanhtml, parser='html')

    d = make_absolute(d, base_url)
    html_filename = '{}.html'.format(canonical_url.replace('/', '_'))
    write_html(d, html_filename)
    return


def main():
    jobs = []
    for ws in WebSite.objects.all():
        # if not ws.title == "Aftonbladet":
        #     continue
        p = multiprocessing.Process(target=save_html, args=(ws,))
        jobs.append(p)
        p.start()


if __name__ == '__main__':
    main()

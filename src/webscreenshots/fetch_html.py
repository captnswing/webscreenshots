#!/usr/bin/env python
#-*- coding: utf-8 -*-
from main.models import WebSite
import hashlib
import multiprocessing
import codecs
from pyquery import PyQuery as pq
import requests
from urlparse import urlparse
from lxml.html import tostring as html2str


def add_base_tag(d, base_url):
    # add (or update) base tag!
    if d('base'):
        d('base').attr['href'] = base_url
    else:
        d('head').append('<base href="{}"'.format(base_url))
    return d


def make_absolute_script(d, base_url):
    for fix_script in d('script[src^="/"]'):
        # prepend base_url to the src value
        absolutepath = base_url.rstrip('/') + '/' + pq(fix_script).attr['src'].lstrip('/')
        pq(fix_script).attr['src'] = absolutepath
    return d


def make_absolute_img(d, base_url):
    for fix_img in d('img[src^="/"]'):
        # prepend base_url to the src value
        absolutepath = base_url.rstrip('/') + '/' + pq(fix_img).attr['src'].lstrip('/')
        pq(fix_img).attr['src'] = absolutepath
    return d


def make_absolute_link(d, base_url):
    for fix_link in d('link[href^="/"]'):
        # prepend base_url to the src value
        absolutepath = base_url.rstrip('/') + '/' + pq(fix_link).attr['href'].lstrip('/')
        pq(fix_link).attr['href'] = absolutepath
    return d


def make_absolute_a(d, base_url):
    # from http://pythonhosted.org/pyquery/tips.html
    # doesn't seem to work
    # d.make_links_absolute(base_url=base_url)
    for fix_a in d('a[href^="/"]'):
        # prepend base_url to the src value
        absolutepath = base_url.rstrip('/') + '/' + pq(fix_a).attr['href'].lstrip('/')
        pq(fix_a).attr['href'] = absolutepath
    return d


def make_relative(d, base_url):
    d = add_base_tag(d, base_url)
    d = make_absolute_script(d, base_url)
    d = make_absolute_link(d, base_url)
    d = make_absolute_a(d, base_url)
    d = make_absolute_img(d, base_url)
    return d


def download_css(filename):
    d = pq(open(filename).read())
    for fixl in d('link[href^="/"]'):
        print pq(fixl).attr['href']


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

    # make relative
    d = make_relative(d, base_url)

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

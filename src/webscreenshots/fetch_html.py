#!/usr/bin/env python
#-*- coding: utf-8 -*-
from main.models import WebSite
import hashlib
import multiprocessing
import requests
import codecs


def save_html(website):
    """thread worker function"""
    canonical_url = website.url.replace('http://', '').replace('www.', '')
    hashed_url = hashlib.md5(canonical_url).hexdigest()
    print 'get:   {}'.format(canonical_url)
    r = requests.get(website.url)
    html = codecs.open('data/{}.html'.format(hashed_url), 'wb', 'utf-8')
    print 'write: {} {}'.format(canonical_url, hashed_url)
    html.write(r.text)
    html.close()
    return


def main():
    jobs = []
    for ws in WebSite.objects.all():
        p = multiprocessing.Process(target=save_html, args=(ws,))
        jobs.append(p)
        p.start()


if __name__ == '__main__':
    main()

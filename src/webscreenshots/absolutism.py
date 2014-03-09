#!/usr/bin/env python
#-*- coding: utf-8 -*-
import unittest
from urlparse import urlsplit
from pyquery import PyQuery as pq


def add_base_tag(d, base_url):
    # add base tag if it doesn't exist
    if not d('base'):
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


def make_absolute(d, base_url):
    d = add_base_tag(d, base_url)
    d = make_absolute_script(d, base_url)
    d = make_absolute_link(d, base_url)
    d = make_absolute_a(d, base_url)
    d = make_absolute_img(d, base_url)
    return d


class TestAbsolute(unittest.TestCase):

    def setUp(self):
        self.base_url = "http://sverigesradio.se/blekinge"
        self.testhtml = open('main/fixtures/simpletest.html', 'r').read()
        self.d = pq(self.testhtml, parser='html')

    def test_make_absolute_a(self):
        before_hrefs = [ pq(h).attr['href'] for h in self.d('a[href]') ]
        # confirm input conditions, all relative links in test html
        self.assertListEqual(['/', ]*len(before_hrefs), [ u[0] for u in before_hrefs ])
        # make link hrefs absolute
        d = make_absolute_a(self.d, self.base_url)
        after_hrefs = [ pq(h).attr['href'] for h in d('a[href]') ]
        # confirm absolute links in test html
        b_scheme = '{}://'.format(urlsplit(self.base_url).scheme)
        self.assertListEqual([b_scheme,]*len(before_hrefs), [ u[0:len(b_scheme)] for u in after_hrefs ])
        # print self.d.outer_html()

    def test_make_absolute_img(self):
        before_src = [ pq(h).attr['src'] for h in self.d('img[src]') ]
        # confirm input conditions, all relative src in test html images
        self.assertListEqual(['/', ]*len(before_src), [ u[0] for u in before_src ])
        # make img src absolute
        d = make_absolute_img(self.d, self.base_url)
        after_src = [ pq(h).attr['src'] for h in d('img[src]') ]
        # confirm absolute src for images in test html
        b_scheme = '{}://'.format(urlsplit(self.base_url).scheme)
        self.assertListEqual([b_scheme,]*len(before_src), [ u[0:len(b_scheme)] for u in after_src ])
        # print self.d.outer_html()

    def test_make_absolute_link(self):
        before_hrefs = [ pq(h).attr['href'] for h in self.d('link[href]') ]
        # confirm input conditions, all relative src in test html images
        self.assertListEqual(['/', ]*len(before_hrefs), [ u[0] for u in before_hrefs ])
        # make img src absolute
        d = make_absolute_link(self.d, self.base_url)
        after_hrefs = [ pq(h).attr['href'] for h in d('link[href]') ]
        # confirm absolute src for images in test html
        b_scheme = '{}://'.format(urlsplit(self.base_url).scheme)
        self.assertListEqual([b_scheme,]*len(after_hrefs), [ u[0:len(b_scheme)] for u in after_hrefs ])
        # print self.d.outer_html()

    def test_make_absolute_script(self):
        before_src = [ pq(h).attr['src'] for h in self.d('script[src]') ]
        # confirm input conditions, all relative src in test html images
        self.assertListEqual(['/', ]*len(before_src), [ u[0] for u in before_src ])
        # make img src absolute
        d = make_absolute_script(self.d, self.base_url)
        after_src = [ pq(h).attr['src'] for h in d('script[src]') ]
        # confirm absolute src for images in test html
        b_scheme = '{}://'.format(urlsplit(self.base_url).scheme)
        self.assertListEqual([b_scheme,]*len(before_src), [ u[0:len(b_scheme)] for u in after_src ])
        #print self.d.outer_html()

    def test_add_base_tag(self):
        # basic test html
        test_html = """<html><head></head><body></body></html>"""
        test_html_with_base = """<html><head><base href="http://test123"></head><body></body></html>"""
        # parse test html
        without_base = pq(test_html, parser='html')
        with_base = pq(test_html_with_base, parser='html')
        # confirm input conditions
        self.assertIsNone(without_base('base').attr['href'])
        self.assertEquals(with_base('base').attr['href'], "http://test123")
        # add / update base tage
        d_with_base = add_base_tag(with_base, self.base_url)
        d_without_base = add_base_tag(without_base, self.base_url)
        # check that base tag exists in head and that it has correct href attribute
        self.assertEquals(d_with_base('base').attr['href'], self.base_url)
        self.assertEquals(d_without_base('base').attr['href'], self.base_url)
        #print self.d.outer_html()


class TestHtmlConversion(unittest.TestCase):

    def setUp(self):
        self.base_url = "http://sverigesradio.se/blekinge"
        self.testhtml = open('main/fixtures/simpletest.html', 'r').read()
        self.d = pq(self.testhtml, parser='html')

    def test_parse_html(self):
        testhtml = open('main/fixtures/simpletest.html', 'r').read()
        d = pq(testhtml, parser='html')
        #print d.outerHtml()

    def test_relative_to_absolute(self):
        d = make_absolute(self.d, self.base_url)
        print d.outer_html()


if __name__ == '__main__':
    unittest.main()

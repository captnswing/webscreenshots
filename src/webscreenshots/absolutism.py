#!/usr/bin/env python
#-*- coding: utf-8 -*-
import unittest
from urlparse import urlsplit
from pyquery import PyQuery as pq
import sys


TEST_HTML = """\
<!DOCTYPE html>
<html lang="sv">

<head>
    <style type="text/css">
        @font-face {
            font-family: Avenir;
            src: url("/relative/avenir.eot") format("eot");
        }
    </style>
    <link rel="stylesheet" href="/relative/stylesheet.css" media="all" type="text/css"/>
    <link rel="image_src" href="/relative/image_head.jpg" type="image/jpeg"/>
    <link rel="apple-touch-icon" href="/relative/apple-touch-icon-default.png" sizes="144x144"/>
    <script src="/relative/javascript_head.js" type="text/javascript"></script>
</head>

<body>
<h1>Hello there!</h1>

<p>some links:</p>
<ol>
    <li>
        <a href="/relative/test1.html">test1</a>
        <a href="/relative/test2.html">test2</a>
        <a href="/relative/test3.html">test3</a>
    </li>
</ol>

<p>some images:</p>
<img src="/relative/image1.png" />
<img src="/relative/image2.png" />
<img src="/relative/image3.png" />

<script src="/relative/javascript_body.js" type="text/javascript"></script>
<script src="http://www.absolute.com/javascript_body.js" type="text/javascript"></script>
</body>
"""


def add_base_tag(d, base_url):
    # add <base> tag if it doesn't exist
    if not d('base'):
        d('head').append('<base href="{}"'.format(base_url))
    return d


def make_all_absolute(d, base_url):
    d = add_base_tag(d, base_url)
    for tag_name, attribute_name in [('script', 'src'), ('link', 'href'), ('a', 'href'), ('img', 'src')]:
        selector = '{}[{}^="/"]'.format(tag_name, attribute_name)
        for fix_tag in d(selector):
            # prepend base_url to the value of attribute with <attribute_name>
            absolutepath = base_url.rstrip('/') + '/' + pq(fix_tag).attr[attribute_name].lstrip('/')
            # replace value of <attribute_name> attribute with new, absolute value
            pq(fix_tag).attr[attribute_name] = absolutepath
    return d


class TestAbsolute(unittest.TestCase):

    def setUp(self):
        self.base_url = "http://www.example.com/test123"
        self.d = pq(TEST_HTML, parser='html')

    def test_add_base_tag(self):
        """test add_base_tag"""
        # basic html as test data
        test_html = """<html><head></head><body></body></html>"""
        # parse test html
        without_base = pq(test_html, parser='html')
        # confirm input conditions
        self.assertIsNone(without_base('base').attr['href'])
        # add base tage
        d_without_base = add_base_tag(without_base, self.base_url)
        # check that base tag exists in head and that it has correct href attribute
        self.assertEquals(d_without_base('base').attr['href'], self.base_url)

    def test_relative_to_absolute(self):
        d = make_all_absolute(self.d, self.base_url)
        print d.outer_html()


if __name__ == '__main__':
    unittest.main()

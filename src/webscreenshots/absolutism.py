#!/usr/bin/env python
#-*- coding: utf-8 -*-
import unittest
from urlparse import urlsplit
from pyquery import PyQuery as pq
import sys


def add_base_tag(d, base_url):
    # add base tag if it doesn't exist
    if not d('base'):
        d('head').append('<base href="{}"'.format(base_url))
    return d


def generate_absolute(tag_name, attribute_name):
    """
    returns a function that makes the relatives links in the <attribute_name> relative
    for the specified <tag_name>
    """
    def make_absolute(d, base_url):
        selector = '{}[{}^="/"]'.format(tag_name, attribute_name)
        for fix_tag in d(selector):
            # prepend base_url to the src value
            absolutepath = base_url.rstrip('/') + '/' + pq(fix_tag).attr[attribute_name].lstrip('/')
            pq(fix_tag).attr[attribute_name] = absolutepath
        return d
    return make_absolute


make_absolute_script = generate_absolute('script', 'src')
make_absolute_link = generate_absolute('link', 'href')
make_absolute_a = generate_absolute('a', 'href')
make_absolute_img = generate_absolute('img', 'src')


def make_all_absolute(d, base_url):
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

    def generate_absolute_test(self, tag_name, attribute_name):
        """
        returns a function that makes the relatives links in the <attribute_name> relative
        for the specified <tag_name>
        """
        def test_make_absolute(self):
            selector = '{}[{}]'.format(tag_name, attribute_name)
            before_hrefs = [ pq(h).attr[attribute_name] for h in self.d(selector) ]
            # confirm input conditions, all relative links in test html
            self.assertListEqual(['/', ]*len(before_hrefs), [ u[0] for u in before_hrefs ])
            # make <attribute_name> values absolute for <tag_name>
            func_name = 'make_absolute_{}'.format(tag_name)
            this_module = sys.modules[__name__]
            d = getattr(this_module, func_name)(self.d, self.base_url)
            after_hrefs = [ pq(h).attr[attribute_name] for h in d(selector) ]
            # confirm absolute links in test html
            b_scheme = '{}://'.format(urlsplit(self.base_url).scheme)
            self.assertListEqual([b_scheme,]*len(before_hrefs), [ u[0:len(b_scheme)] for u in after_hrefs ])
            #print self.d.outer_html()
        return test_make_absolute

    def test_a(self):
        test_make_absolute_a = self.generate_absolute_test('a', 'href')
        test_make_absolute_a(self)

    def test_script(self):
        test_make_absolute_script = self.generate_absolute_test('script', 'src')
        test_make_absolute_script(self)

    def test_link(self):
        test_make_absolute_link = self.generate_absolute_test('link', 'href')
        test_make_absolute_link(self)

    def test_img(self):
        test_make_absolute_img = self.generate_absolute_test('img', 'src')
        test_make_absolute_img(self)

    def test_add_base_tag(self):
        # basic test html
        test_html = """<html><head></head><body></body></html>"""
        # parse test html
        without_base = pq(test_html, parser='html')
        # confirm input conditions
        self.assertIsNone(without_base('base').attr['href'])
        # add / update base tage
        d_without_base = add_base_tag(without_base, self.base_url)
        # check that base tag exists in head and that it has correct href attribute
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
        d = make_all_absolute(self.d, self.base_url)
        print d.outer_html()


if __name__ == '__main__':
    unittest.main()

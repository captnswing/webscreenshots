#!/usr/bin/env python
#-*- coding: utf-8 -*-
import unittest
from pyquery import PyQuery as pq
from fetch_html import download_css, make_absolute, add_base_tag


class TestUrlConversion(unittest.TestCase):

    def setUp(self):
        self.base_url = "http://sverigesradio.se/blekinge"
        self.testhtml = open('main/fixtures/simpletest.html', 'r').read()
        self.testcss = open('main/fixtures/test.css', 'r').read()
        self.d = pq(self.testhtml, parser='html')

    def test_make_absolute_script_urls(self):
        d = make_absolute(self.d, self.base_url)
        #print d.outerHtml()

    def test_add_base_tag(self):
        # basic test html
        test_html = """<html><head></head><body></body></html>"""
        test_html_with_base = """<html><head><base href="http://test123"></head><body></body></html>"""
        # parse test html
        without_base = pq(test_html, parser='html')
        with_base = pq(test_html_with_base, parser='html')
        # confirm input conditions
        self.assertIsNone(without_base.attr['href'])
        self.assertEquals(with_base('base').attr['href'], "http://test123")
        # add / update base tage
        d_with_base = add_base_tag(with_base, self.base_url)
        d_without_base = add_base_tag(without_base, self.base_url)
        # check that base tag exists in head and that it has correct href attribute
        self.assertEquals(d_with_base('base').attr['href'], self.base_url)
        self.assertEquals(d_without_base('base').attr['href'], self.base_url)

    def test_css_urls(self):
        pass
        #print self.testcss

    def test_parse_html(self):
        testhtml = open('main/fixtures/simpletest.html', 'r').read()
        d = pq(testhtml, parser='html')
        #print d.outerHtml()



def main():
    filename = "data/aftonbladet.se.html"
    download_css(filename)


if __name__ == '__main__':
    unittest.main()
    #main()

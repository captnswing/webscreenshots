#!/usr/bin/env python
#-*- coding: utf-8 -*-
import unittest
from pyquery import PyQuery as pq


class TestUrlConversion(unittest.TestCase):

    def setUp(self):
        self.testhtml = open('data/sverigesradio.se_blekinge.html', 'r').read()
        self.d = pq(self.testhtml)
        self.testcss = open('data/sr.responsive.min.css', 'r').read()

    def test_script_urls(self):
        # finds all script tags that have a src attribute whose value starts with '/'
        for fixs in self.d('script[src^="/"]'):
            print "*"*50
            absolutePath = "http://sverigesradio.se" + pq(fixs).attr['src']
            pq(fixs).attr['src'] = absolutePath
            #print pq(fixs).attr['src']
        #print self.d.html()

    def test_css_urls(self):
        print self.testcss

if __name__ == '__main__':
    unittest.main()

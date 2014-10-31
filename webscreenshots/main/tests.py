# -*- coding: utf-8 -*-
import datetime
import tempfile
import os

from django.utils import unittest
from django.test import TestCase, Client
from django.core.urlresolvers import reverse

from webscreenshots.main.views import get_sites_for_day, get_adjacent_times
from webscreenshots.celerytasks import upload_files
from webscreenshots.utils import get_slice_from_list, calculate_expexted_times, roundTime


class TestViewsModule(TestCase):
    fixtures = ['newsites.json']

    def setUp(self):
        self.c = Client()

    def test_post(self):
        response = self.c.post('/2013-01-14/', {'sites[]': ('aftonbladet.se', 'svt.se')})
        self.assertEqual(response.status_code, 200)

    def test_permalink_url(self):
        testurl = reverse('home-datetime', args=('2013-01-14', '17.54'))
        self.assertEqual(testurl, '/2013-01-14/17.54/')
        response = self.c.get(testurl)
        self.assertEqual(response.status_code, 200)

    def test_home(self):
        testurl = reverse('home-date', args=('2013-01-14',))
        response = self.c.get(testurl)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')

    def test_real_slice(self):
        print get_adjacent_times(datetime.datetime(2013, 04, 22, 23, 33))

    def test_get_sites_for_day(self):
        print get_sites_for_day(datetime.datetime.today())

    def test_s3_upload(self):
        with tempfile.NamedTemporaryFile("wb", delete=False) as myfile:
            filename = myfile.name
            myfile.write("testdata")
        upload_files(filename)
        os.remove(filename)


class TestUtilsModule(unittest.TestCase):
    def setUp(self):
        self.c = Client()
        self.testlist = range(10)
        self.dt = datetime.datetime(2013, 4, 22, 17, 23, 12)
        self.et = ['23.00', '00.00', '01.00', '02.00', '03.00', '04.00', '05.00', '06.00']
        minutes = ['00', '05', '10', '15', '20', '25', '30', '35', '40', '45', '50', '55']
        hours = ['07', '08', '09', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22']
        self.et += ["{}.{}".format(h, m) for h in hours for m in minutes]
        self.et = sorted(self.et)

    def test_get_slice_from_list(self):
        self.assertListEqual([0, 1, 2, 3, 4], get_slice_from_list(self.testlist, 2, 2))
        self.assertListEqual([3, 4, 5, 6, 7], get_slice_from_list(self.testlist, 5, 2))
        self.assertListEqual([9, 0, 1, 2, 3], get_slice_from_list(self.testlist, 1, 2))
        self.assertListEqual([8, 9, 0, 1, 2], get_slice_from_list(self.testlist, 0, 2))
        self.assertListEqual([8, 9, 0, 1, 2, 3, 4], get_slice_from_list(self.testlist, 1, 3))
        self.assertListEqual([7, 8, 9, 0, 1], get_slice_from_list(self.testlist, 9, 2))
        self.assertListEqual([4, 5, 6, 7, 8, 9, 0], get_slice_from_list(self.testlist, 7, 3))

    def test_calculate_expexted_times(self):
        self.assertListEqual(self.et, calculate_expexted_times())

    def test_roundTime(self):
        self.assertEqual(datetime.datetime(2013, 4, 22, 17, 0, 0), roundTime(self.dt, roundTo=60 * 60))
        self.assertEqual(datetime.datetime(2013, 4, 22, 17, 25, 0), roundTime(self.dt))

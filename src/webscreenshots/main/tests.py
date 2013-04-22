from django.utils import unittest
from models import WebSite
from views import get_sitechunks, get_sites_for_day, get_adjacent_times
from django.test import TestCase, Client
import datetime
from webscreenshots.celerytasks import upload_files
from django.core.urlresolvers import reverse
from main.utils import get_slice_from_list, calculate_expexted_times, roundTime
import tempfile
import os


class TestViewsModule(TestCase):
    fixtures = ['newsites.json']

    def setUp(self):
        self.c = Client()

    def test_post(self):
        response = self.c.post('/2013-01-14/', {'sites[]': ('aftonbladet.se', 'svt.se')})
        print response.status_code

    def test_permalink_url(self):
        print reverse('home-datetime', args=('2013-01-14', '17.54'))
        testurl = '/2013-01-14/17.54/'
        print testurl
        response = self.c.get(testurl)
        print response.status_code

    def test_real_slice(self):
        print get_adjacent_times(datetime.datetime(2013, 04, 22, 23, 33))

    def test_chunks(self):
        sitesforday = WebSite.objects.values('title', 'category')
        allchunks = get_sitechunks(sitesforday)
        for c in allchunks:
            print c

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

    def test_slice_list(self):
        self.assertListEqual([0, 1, 2, 3, 4], get_slice_from_list(self.testlist, 2, 2))
        self.assertListEqual([3, 4, 5, 6, 7], get_slice_from_list(self.testlist, 5, 2))
        self.assertListEqual([8, 9, 0, 1, 2], get_slice_from_list(self.testlist, 0, 2))
        self.assertListEqual([9, 0, 1, 2, 3], get_slice_from_list(self.testlist, 1, 2))
        self.assertListEqual([8, 9, 0, 1, 2, 3, 4], get_slice_from_list(self.testlist, 1, 3))
        self.assertListEqual([7, 8, 9, 0, 1], get_slice_from_list(self.testlist, 9, 2))
        self.assertListEqual([4, 5, 6, 7, 8, 9, 0], get_slice_from_list(self.testlist, 7, 3))

    def test_calculate_expexted_times(self):
        print calculate_expexted_times()

    def test_roundTime(self):
        self.assertEqual(datetime.datetime(2013, 4, 22, 17, 0, 0), roundTime(self.dt, roundTo=60*60))
        self.assertEqual(datetime.datetime(2013, 4, 22, 17, 25, 0), roundTime(self.dt))

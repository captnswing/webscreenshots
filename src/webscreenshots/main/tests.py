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
        self.et = ['00.00', '01.00', '02.00', '03.00', '04.00', '05.00', '06.00', '07.00', '07.05', '07.10', '07.15',
            '07.20', '07.25', '07.30', '07.35', '07.40', '07.45', '07.50', '07.55', '08.00', '08.05', '08.10',
            '08.15', '08.20', '08.25', '08.30', '08.35', '08.40', '08.45', '08.50', '08.55', '09.00', '09.05',
            '09.10', '09.15', '09.20', '09.25', '09.30', '09.35', '09.40', '09.45', '09.50', '09.55', '10.00',
            '10.05', '10.10', '10.15', '10.20', '10.25', '10.30', '10.35', '10.40', '10.45', '10.50', '10.55',
            '11.00', '11.05', '11.10', '11.15', '11.20', '11.25', '11.30', '11.35', '11.40', '11.45', '11.50',
            '11.55', '12.00', '12.05', '12.10', '12.15', '12.20', '12.25', '12.30', '12.35', '12.40', '12.45',
            '12.50', '12.55', '13.00', '13.05', '13.10', '13.15', '13.20', '13.25', '13.30', '13.35', '13.40',
            '13.45', '13.50', '13.55', '14.00', '14.05', '14.10', '14.15', '14.20', '14.25', '14.30', '14.35',
            '14.40', '14.45', '14.50', '14.55', '15.00', '15.05', '15.10', '15.15', '15.20', '15.25', '15.30',
            '15.35', '15.40', '15.45', '15.50', '15.55', '16.00', '16.05', '16.10', '16.15', '16.20', '16.25',
            '16.30', '16.35', '16.40', '16.45', '16.50', '16.55', '17.00', '17.05', '17.10', '17.15', '17.20',
            '17.25', '17.30', '17.35', '17.40', '17.45', '17.50', '17.55', '18.00', '18.05', '18.10', '18.15',
            '18.20', '18.25', '18.30', '18.35', '18.40', '18.45', '18.50', '18.55', '19.00', '19.05', '19.10',
            '19.15', '19.20', '19.25', '19.30', '19.35', '19.40', '19.45', '19.50', '19.55', '20.00', '20.05',
            '20.10', '20.15', '20.20', '20.25', '20.30', '20.35', '20.40', '20.45', '20.50', '20.55', '21.00',
            '21.05', '21.10', '21.15', '21.20', '21.25', '21.30', '21.35', '21.40', '21.45', '21.50', '21.55',
            '22.00', '22.05', '22.10', '22.15', '22.20', '22.25', '22.30', '22.35', '22.40', '22.45', '22.50',
            '22.55', '23.00']

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

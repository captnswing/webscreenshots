from django.utils import unittest
from models import WebSite
from views import get_sitechunks, get_sites_for_day
from django.test import TestCase, Client
import datetime
from webscreenshots.celerytasks import upload_files


class ViewTest(unittest.TestCase):

    def setUp(self):
        self.c = Client()

    def test_post(self):
        response = self.c.post('/2013-01-04/', {'sites[]': ('aftonbladet.se', 'svt.se')})
        print response.status_code


class MiscTest(TestCase):

    fixtures = ['newsites.json']

    def test_chunks(self):
        sitesforday = WebSite.objects.values('title', 'category')
        allchunks = get_sitechunks(sitesforday)
        for c in allchunks:
            print c

    def test_get_sites_for_day(self):
        print get_sites_for_day(datetime.datetime.today())

    def test_s3_upload(self):
        upload_files('manage.py')

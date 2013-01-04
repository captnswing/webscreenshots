import os
os.environ["DJANGO_SETTINGS_MODULE"] = "webscreenshots.settings"
from django.utils import unittest
from django.test import Client
import json


class ViewTest(unittest.TestCase):

    def setUp(self):
        self.c = Client()

    def test_post(self):
        myjson_response = self.c.post('/2013-01-04/', {'sites[]': ('aftonbladet.se', 'svt.se')})
        print json.loads(myjson_response.content)

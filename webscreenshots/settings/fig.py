# -*- coding: utf-8 -*-
# settings/fig.py
import os
import sys
from .base import *
from fnmatch import fnmatch

DEBUG = True
TEMPLATE_DEBUG = DEBUG
WEBSCREENSHOTS_IMAGES_PATH = '/wsimages_dev'
CELERYD_LOGPATH = root('../../celerylogs')
S3_BUCKET_NAME = "webscreenshots-test"

try:
    AWS_ACCESS_KEY = os.environ['AWS_ACCESS_KEY']
    AWS_SECRET_KEY = os.environ['AWS_SECRET_KEY']
except KeyError:
    print "you need to set the environment variables AWS_ACCESS_KEY and AWS_SECRET_KEY"
    sys.exit(-1)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'postgres',
        'USER': 'postgres',
        'HOST': 'db',
        'PORT': 5432,
    },
}


# from http://djangosnippets.org/snippets/1380/
class glob_list(list):
    def __contains__(self, key):
        for elt in self:
            if fnmatch(key, elt):
                return True
        return False


INTERNAL_IPS = glob_list([
    '127.0.0.1',
    '10.0.*.*'
])

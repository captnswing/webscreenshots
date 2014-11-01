# settings/frank.py
from .base import *
from fnmatch import fnmatch

DEBUG = True
TEMPLATE_DEBUG = DEBUG
WEBSCREENSHOTS_IMAGES_PATH = '/wsimages_dev'
CELERYD_LOGPATH = "." #root('../../celerylogs')
S3_BUCKET_NAME = "svti-webscreenshots-test"
AWS_ACCESS_KEY = "AKIAJFHPRRM3PUMAEATQ"
AWS_SECRET_KEY = "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"
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'postgres',
        'USER': 'postgres',
        'HOST': 'db',
        'PORT': 5432,
    },
    # 'default': {
    #     'ENGINE': 'django.db.backends.postgresql_psycopg2',
    #     'NAME': 'postgres',
    #     'USER': 'hoffsummer',
    #     'PASSWORD': 'mp109',
    #     'HOST': 'localhost',
    #     'PORT': '',
    # }
}

# from http://djangosnippets.org/snippets/1380/
class glob_list(list):
    def __contains__(self, key):
        for elt in self:
            if fnmatch(key, elt): return True
        return False

INTERNAL_IPS = glob_list([
    '127.0.0.1',
    '10.0.*.*'
])

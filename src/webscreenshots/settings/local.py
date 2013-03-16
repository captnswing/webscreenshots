# settings/local.py
from .base import *
from fnmatch import fnmatch
DEBUG = True
TEMPLATE_DEBUG = DEBUG
WEBSCREENSHOTS_IMAGES_PATH = '/wsimages_dev'
CELERYD_LOGPATH = ''

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

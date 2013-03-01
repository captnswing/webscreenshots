# settings/local.py
from .base import *
DEBUG = True
TEMPLATE_DEBUG = True
# from http://djangosnippets.org/snippets/1380/
from fnmatch import fnmatch
class glob_list(list):
    def __contains__(self, key):
        for elt in self:
            if fnmatch(key, elt): return True
        return False

INTERNAL_IPS = glob_list([
    '127.0.0.1',
    '10.0.*.*'
])

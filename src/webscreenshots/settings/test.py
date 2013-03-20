# settings/prod.py
from .base import *
DEBUG = True
TEMPLATE_DEBUG = DEBUG
S3_BUCKET_NAME = "svti-webscreenshots.test"

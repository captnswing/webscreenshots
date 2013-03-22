# settings/prod.py
from .base import *
DEBUG = True
TEMPLATE_DEBUG = DEBUG
S3_BUCKET_NAME = "svti-webscreenshots.test"
AWS_ACCESS_KEY = "AKIAISDWNLO33JF3NIRA"
AWS_SECRET_KEY = "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"

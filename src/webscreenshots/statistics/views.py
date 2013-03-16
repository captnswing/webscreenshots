#-*- coding: utf-8 -*-
from django.http import HttpResponseRedirect, HttpResponse
import json
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from boto.s3.connection import S3Connection
import datetime
from django.conf import settings
from django.views.decorators.cache import cache_page


def main(request):
    return render_to_response('statistics.html', {
    }, context_instance=RequestContext(request))

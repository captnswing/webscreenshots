#-*- coding: utf-8 -*-
from django.http import HttpResponseRedirect, HttpResponse
import json
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from boto.s3.connection import S3Connection
import datetime
from django.conf import settings
from django.views.decorators.cache import cache_page


def get_sites_for_day(selected_day):
    conn = S3Connection()
    bucket = conn.get_bucket('svti-webscreenshots')
    selected_day = selected_day.strftime("%Y/%m/%d")
    keys = bucket.get_all_keys(prefix=selected_day + "/", delimiter="/")
    sites = [key.name.lstrip(selected_day).rstrip("/").replace('|', '/') for key in keys]
    return sites


@cache_page(60 * 15)
def fake_wsimages(request):
    from PIL import Image, ImageDraw, ImageFont
    site = request.path_info.split('/')[-2].replace('|', '/')
    im = Image.new('RGBA', (220,220), (100, 100, 100, 100))
    draw = ImageDraw.Draw(im)
    font = ImageFont.truetype("/usr/share/fonts/truetype/msttcorefonts/arial.ttf", 20)
    text_pos = (30,100)
    draw.text(text_pos, site, fill=(255,255,255), font=font)
    response = HttpResponse(mimetype="image/png")
    im.save(response, 'PNG')
    return response


# from http://stackoverflow.com/a/312464/41404
def chunks(l, n):
    """ Yield successive n-sized chunks from l.
    """
    for i in xrange(0, len(l), n):
        yield l[i:i + n]


def home(request, pubdate=None):
    thumbwidth = request.REQUEST.get("thumbwidth", 220)
    lens = request.REQUEST.get("lens", "on")
    firstdataday = datetime.datetime(2013, 1, 4)
    today = datetime.datetime.today()
    if not pubdate:
        d = today
    else:
        y, m, d = pubdate.split('-')
        d = datetime.datetime(int(y), int(m), int(d))
        # if specified date is todays'
        if d.timetuple()[:3] == today.timetuple()[:3]:
            d = today
    if d < firstdataday:
        return HttpResponseRedirect('/%s' % firstdataday.strftime("%Y-%m-%d"))
    if d > today:
        return HttpResponseRedirect('/%s' % today.strftime("%Y-%m-%d"))

    keyname = "sites_%s" % d.strftime("%Y-%m-%d")
    if keyname in request.session:
        sitesforday = request.session[keyname]
    else:
        sitesforday = get_sites_for_day(d)
        request.session[keyname] = sitesforday

    sites = [ r[0] for r in request.REQUEST.items() if r[1] == 'on' ]
    if not sites:
        sites = ["aftonbladet.se", "dn.se", "svt.se/nyheter"]

    offhours = [23, 0, 1, 2, 3, 4, 5, 6]

    return render_to_response('home.html', {
        'thumbwidth': thumbwidth,
        'loupe': lens,
        'offhours': json.dumps(offhours),
        'first_data_day': firstdataday.ctime(),
        'selected_day': d.ctime(),
        'selected_sites': sites,
        'selected_sites_json': json.dumps(sites),
        'wsimages_path': settings.WEBSCREENSHOTS_IMAGES_PATH,
        'allsites': chunks(sitesforday, 8),
    }, context_instance=RequestContext(request))

#-*- coding: utf-8 -*-
import json
import datetime
from django.http import HttpResponseRedirect, HttpResponse, HttpResponseServerError
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from boto import connect_s3
from django.conf import settings
from django.views.decorators.cache import cache_page
from django.template import Context, loader
from models import WebSite, CATEGORY_CHOICES
from utils import calculate_expexted_times, roundTime, get_slice_from_list


def get_adjacent_times(datetime):
    et = calculate_expexted_times()
    kl = datetime.strftime("%H.%M")
    if kl not in et:
        rounded_to_5min = roundTime(datetime)
        kl = rounded_to_5min.strftime("%H.%M")
    if kl not in et:
        rounded_to_60min = roundTime(datetime, roundTo=60*60)
        kl = rounded_to_60min.strftime("%H.%M")
    idx = et.index(kl)
    return get_slice_from_list(et, idx, 4)


def permalink(request, pubdate=None, pubtime=None):
    return HttpResponse('')


def get_sites_for_day(selected_day):
    conn = connect_s3(settings.AWS_ACCESS_KEY, settings.AWS_SECRET_KEY)
    bucket = conn.get_bucket(settings.S3_BUCKET_NAME)
    selected_day = selected_day.strftime("%Y/%m/%d")
    keys = bucket.get_all_keys(prefix=selected_day + "/", delimiter="/")
    sites = [key.name.lstrip(selected_day).rstrip("/").replace('|', '/') for key in keys]
    return sites


def server_error(request):
    """
    custom 500 error handler, that includes STATIC_URL in context
    """
    t = loader.get_template('500.html')
    return HttpResponseServerError(t.render(Context({
        'STATIC_URL': settings.STATIC_URL
    })))


@cache_page(60 * 15)
def fake_wsimages(request):
    from PIL import Image, ImageDraw, ImageFont

    site = request.path_info.split('/')[-2].replace('|', '/')
    im = Image.new('RGBA', (220, 220), (100, 100, 100, 100))
    draw = ImageDraw.Draw(im)
    font = ImageFont.truetype("/usr/share/fonts/truetype/msttcorefonts/arial.ttf", 20)
    text_pos = (30, 100)
    draw.text(text_pos, site, fill=(255, 255, 255), font=font)
    response = HttpResponse(mimetype="image/png")
    im.save(response, 'PNG')
    return response


# from http://stackoverflow.com/a/312464/41404
def chunks(l, n):
    """ Yield successive n-sized chunks from l.
    """
    for i in xrange(0, len(l), n):
        yield l[i:i + n]


def get_sitechunks(allsites):
    sitesforday = [e.values() for e in allsites]
    categories = dict(CATEGORY_CHOICES)
    sitesforday = [(categories[a], b) for a, b in sitesforday]
    international = [s for s in sitesforday if s[0] == categories['1']]
    riks = [s for s in sitesforday if s[0] == categories['2']]
    regionala = [s for s in sitesforday if s[0] == categories['3']]
    allchunks = [international, riks]
    for rc in chunks(regionala, 25):
        allchunks.append(rc)
    return allchunks


def home(request, pubdate=None):
    thumbwidth = request.REQUEST.get("thumbwidth", 220)
    lens = request.REQUEST.get("lens", "on")
    firstdataday = datetime.datetime(2013, 1, 4)
    today = datetime.datetime.today()
    if not pubdate:
        d = today
    else:
        d = datetime.datetime.strptime(pubdate, "%Y-%m-%d")
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

    selected_sites = [r[0] for r in request.REQUEST.items() if r[1] == 'on']
    if not selected_sites:
        sites = ["aftonbladet.se", "dn.se", "svt.se/nyheter"]

    offhours = [23, 0, 1, 2, 3, 4, 5, 6]
    sitechunks = get_sitechunks(WebSite.objects.values('title', 'category'))

    return render_to_response('home.html', {
        'thumbwidth': thumbwidth,
        'loupe': lens,
        'offhours': json.dumps(offhours),
        'first_data_day': firstdataday.ctime(),
        'selected_day': d.ctime(),
        'selected_sites': selected_sites,
        'selected_sites_json': json.dumps(sites),
        'wsimages_path': settings.WEBSCREENSHOTS_IMAGES_PATH,
        'allsites': sitechunks,
        'currentday': d
    }, context_instance=RequestContext(request))


if __name__ == '__main__':
    sitesforday = WebSite.objects.values('title', 'category')
    print sitesforday

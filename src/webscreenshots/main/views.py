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
from models import WebSite
from utils import calculate_expexted_times, roundTime, get_slice_from_list
from PIL import Image, ImageDraw, ImageFont


def get_adjacent_times(datetime):
    et = calculate_expexted_times()
    kl = datetime.strftime("%H.%M")
    if kl not in et:
        rounded_to_5min = roundTime(datetime, roundTo=5*60)
        kl = rounded_to_5min.strftime("%H.%M")
    if kl not in et:
        rounded_to_60min = roundTime(datetime, roundTo=60*60)
        kl = rounded_to_60min.strftime("%H.%M")
    idx = et.index(kl)
    return get_slice_from_list(et, idx, 5)


def get_sites_for_day(selected_day):
    conn = connect_s3(settings.AWS_ACCESS_KEY, settings.AWS_SECRET_KEY)
    bucket = conn.get_bucket(settings.S3_BUCKET_NAME)
    selected_day = selected_day.strftime("%Y/%m/%d")
    keys = bucket.get_all_keys(prefix=selected_day + "/", delimiter="/")
    sites = [key.name.lstrip(selected_day).rstrip("/") for key in keys]
    ws = [ws for ws in WebSite.objects.all() if ws.canonicalurl in sites]
    return ws


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
    """ yield successive n-sized chunks from l.
    """
    for i in xrange(0, len(l), n):
        yield l[i:i + n]


def home(request, pubdate=None, pubtime=None):
    thumbwidth = request.REQUEST.get("thumbwidth", 220)
    lens = request.REQUEST.get("lens", "on")
    firstdataday = datetime.datetime(2013, 1, 4)
    today = datetime.datetime.today()
    if not pubtime:
        pubtime = '00.00'
    if not pubdate:
        d = today
    else:
        try:
            d = datetime.datetime.strptime(pubdate+pubtime, "%Y-%m-%d/%H.%M")
        except ValueError:
            d = datetime.datetime.strptime(pubdate, "%Y-%m-%d")
        # if specified date is todays'
        if d.timetuple()[:3] == today.timetuple()[:3]:
            d = today
    if d < firstdataday:
        return HttpResponseRedirect('/%s' % firstdataday.strftime("%Y-%m-%d"))
    if d > today:
        return HttpResponseRedirect('/%s' % today.strftime("%Y-%m-%d"))

    sitesforday = get_sites_for_day(d)

    # keyname = "sites_%s" % d.strftime("%Y-%m-%d")
    # print request.session
    # if keyname in request.session:
    #     sitesforday = request.session[keyname]
    #     print sitesforday
    # else:
    #     sitesforday = get_sites_for_day(d)
    #     request.session[keyname] = sitesforday

    selected_sites = [r[0] for r in request.REQUEST.items() if r[1] == 'on']
    if not selected_sites:
        selected_sites = ["aftonbladet.se", "dn.se", "svt.se|nyheter"]

    offhours = [23, 0, 1, 2, 3, 4, 5, 6]

    return render_to_response('index.html', {
        'thumbwidth': thumbwidth,
        'loupe': lens,
        'offhours': json.dumps(offhours),
        'first_data_day': firstdataday.ctime(),
        'selected_day': d.ctime(),
        'selected_sites': selected_sites,
        'selected_sites_json': json.dumps(selected_sites),
        'wsimages_path': settings.WEBSCREENSHOTS_IMAGES_PATH,
        'availablesites': chunks(sitesforday, 10),
        'currentday': d
    }, context_instance=RequestContext(request))


if __name__ == '__main__':
    sitesforday = WebSite.objects.values('title', 'category')
    print sitesforday

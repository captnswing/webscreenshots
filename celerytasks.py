from __future__ import absolute_import
import time
import datetime
import subprocess
from urlparse import urlsplit

from celery.utils.log import get_task_logger
import os
from boto.s3.connection import S3Connection
from boto.s3.key import Key

from celeryapp import celery
from celery import chain

os.environ["DJANGO_SETTINGS_MODULE"] = "settings"
from main.models import WebSite


logger = get_task_logger(__name__)
BUCKET_NAME = "svti-webscreenshots"


@celery.task(name='celerytasks.remove_file')
def remove_file(filename):
    logger.info("removing %s" % filename)
    os.remove(filename)


@celery.task(name='celerytasks.upload_file')
def upload_file(filename):
    logger.info(filename.split('__')[-1])
    # TODO: change these to bucket specific credentials
    AWS_ACCESS_KEY = os.environ["AWS_ACCESS_KEY"]
    AWS_SECRET_KEY = os.environ["AWS_SECRET_KEY"]
    conn = S3Connection(AWS_ACCESS_KEY, AWS_SECRET_KEY)
    bucket = conn.get_bucket(BUCKET_NAME)
    k = Key(bucket)
    logger.info('Uploading %s to Amazon S3 bucket %s' % (filename, BUCKET_NAME))
    k.key = filename.replace('images/', '').replace('-full.png', '.png').replace('__', '/')
    k.set_contents_from_filename(filename)
    return filename

#    elif size == "M":
#        webkit2png_cmd = webkit2png_cmdbase + """ -C --clipwidth=1280 --clipheight=1280 -s 1.0 -o '{1}' {2}"""
#        fileext = "-clipped.png"
#    elif size == "T":
#        webkit2png_cmd = webkit2png_cmdbase + """ -C --clipwidth=640 --clipheight=640 -s 0.5 -o '{1}' {2}"""
#        fileext = "-clipped.png"


@celery.task(name='celerytasks.fetch_webscreenshot')
def fetch_webscreenshot(url, dry_run=False):
    user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.8; rv:15.0) Gecko/20100101 Firefox/15.0.1'
    timestamp = str(int(time.mktime(datetime.datetime.now().timetuple())))
    webkit2png_cmd = """./webkit2png --user-agent='{0}' -W 1280 -H 1280 -D images -F -o '{1}' {2}"""
    webkit2png_cmd += """ 2>&1 >/dev/null"""
    fileext = "-full.png"
    parsed = urlsplit(url)
    canonicalurl = parsed.netloc.lstrip('www.')
    urlpath = parsed.path.strip('/')
    if urlpath:
        canonicalurl += "-" + urlpath.replace('/', '-')
    canonicalurl += "-" + timestamp
    filename = datetime.date.today().strftime("%Y__%m__%d") + "__" + canonicalurl
    webkit2png_cmd = webkit2png_cmd.format(user_agent, filename, url)
    if dry_run:
        logger.info(webkit2png_cmd)
        return os.path.join("images", filename + fileext)
    ret = subprocess.call(webkit2png_cmd, shell=True)
    if ret != 0:
        raise IOError("unable to fetch '{0}', failed with return code {1}.".format(url, ret))
    return os.path.join("images", filename + fileext)


if __name__ == '__main__':
    for ws in WebSite.objects.all():
        print fetch_webscreenshot(ws.url, dry_run=True)
        res = chain(fetch_webscreenshot.s(ws.url), upload_file.s(), remove_file.s())()

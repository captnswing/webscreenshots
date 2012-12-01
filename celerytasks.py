from __future__ import absolute_import
from celery import chain
from celery.utils.log import get_task_logger
from celeryapp import celery
import os
import time
import datetime
from boto.s3.connection import S3Connection
from boto.s3.key import Key
import subprocess


logger = get_task_logger(__name__)
BUCKET_NAME = "svti-webscreenshots"


@celery.task(name='celerytasks.remove_files')
def remove_files(filenames):
    for fn in filenames:
        logger.info("removing %s" % fn)
#        os.remove(fn)


@celery.task(name='celerytasks.upload_files')
def upload_files(filenames):
    # TODO: change these to bucket specific credentials
    AWS_ACCESS_KEY = os.environ["AWS_ACCESS_KEY"]
    AWS_SECRET_KEY = os.environ["AWS_SECRET_KEY"]
    conn = S3Connection(AWS_ACCESS_KEY, AWS_SECRET_KEY)
    bucket = conn.get_bucket(BUCKET_NAME)
    k = Key(bucket)
    for fn in filenames:
        logger.info('Uploading %s to Amazon S3 bucket %s' % (fn, BUCKET_NAME))
        k.key = os.path.join(datetime.date.today().strftime("%Y/%m"), os.path.basename(fn))
        k.set_contents_from_filename(fn)
    return filenames


@celery.task(name='celerytasks.fetch_webscreenshot')
def fetch_webscreenshot(url):
    USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.8; rv:15.0) Gecko/20100101 Firefox/15.0.1'
    now = datetime.datetime.now()
    timestamp = str(int(time.mktime(now.timetuple())))
    PNG_CMD_TEMPLATE = """./webkit2png --user-agent='{0}' -o '{1}' -FC {2} 2>&1 >/dev/null"""
    webkit2png_cmd = PNG_CMD_TEMPLATE.format(USER_AGENT, os.path.join("images", timestamp), url)
    ret = subprocess.call(webkit2png_cmd, shell=True)
    if ret != 0:
        raise IOError("Command failed with return code", ret)
#    dirname = os.path.join(url.strip('http://'), datetime.date.today().strftime("%Y/%m"))
    filenames = [ 'images/{0}-{1}.png'.format(timestamp, filetype) for filetype in ('clipped', 'full') ]
    return filenames


if __name__ == '__main__':
    res = chain(fetch_webscreenshot.s("http://svt.se"), upload_files.s(), remove_files.s())()
    res.get()

from __future__ import absolute_import
from celeryapp import celery
import os
import time
import datetime
import sys
from boto.s3.connection import S3Connection
from boto.s3.key import Key
import subprocess


def percent_cb(complete, total):
    sys.stdout.write('.')
    sys.stdout.flush()


@celery.task(name='celerytasks.add')
def add(x, y):
    return x + y

# TODO: change these to bucket specific credentials
AWS_ACCESS_KEY = os.environ["AWS_ACCESS_KEY"]
AWS_SECRET_KEY = os.environ["AWS_SECRET_KEY"]
BUCKET_NAME = "svti-webscreenshots"
USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.8; rv:15.0) Gecko/20100101 Firefox/15.0.1'


@celery.task(name='celerytasks.upload_file')
def upload_file(filename, dirname, bucketname):
    print filename
    conn = S3Connection(AWS_ACCESS_KEY, AWS_SECRET_KEY)
    bucket = conn.get_bucket(bucketname)
    print 'Uploading %s to Amazon S3 bucket %s' % (filename, bucketname)
    k = Key(bucket)
    k.key = os.path.join(dirname, filename)
    k.set_contents_from_filename(filename, cb=percent_cb, num_cb=10)
    os.remove(filename)


@celery.task(name='celerytasks.fetch_webscreenshot')
def fetch_webscreenshot(url):
    now = datetime.datetime.now()
    timestamp = str(int(time.mktime(now.timetuple())))
    PNG_CMD_TEMPLATE = """pwd;./webkit2png --user-agent='{0}' -o '{1}' -FC {2}"""
    webkit2png_cmd = PNG_CMD_TEMPLATE.format(USER_AGENT, os.path.join("images", timestamp), url)
    print webkit2png_cmd
    subprocess.call(webkit2png_cmd, shell=True)
    dirname = os.path.join(url.strip('http://'), datetime.date.today().strftime("%Y/%m"))
#    for filetype in ['clipped', 'full']:
#        filename = '{0}-{1}.png'.format(timestamp, filetype)
#        print filename
#        result = upload_file.delay(filename, dirname, BUCKET_NAME)


if __name__ == '__main__':
    res = add.delay(12, 2)
    res.get(timeout=1)
    res = fetch_webscreenshot.delay("http://svt.se")
    res.get(timeout=5)

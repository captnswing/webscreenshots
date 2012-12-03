from __future__ import absolute_import
import time
import datetime
import subprocess
from urlparse import urlsplit
from PIL import Image
import types
from celery.utils.log import get_task_logger
import os
from boto.s3.connection import S3Connection
from boto.s3.key import Key
from celeryapp import celery
os.environ["DJANGO_SETTINGS_MODULE"] = "settings"
from main.models import WebSite


logger = get_task_logger(__name__)
BUCKET_NAME = "svti-webscreenshots"


@celery.task(name='celerytasks.remove_files')
def remove_files(filenames):
    if not isinstance(filenames, types.ListType):
        filenames = list(filenames)
    for fn in filenames:
        logger.info("removing %s" % fn)
        os.remove(fn)


@celery.task(name='celerytasks.upload_files')
def upload_files(filenames):
    if not isinstance(filenames, types.ListType):
        filenames = list(filenames)
    for fn in filenames:
        logger.info(fn.split('__')[-1])
        # TODO: change these to bucket specific credentials
        AWS_ACCESS_KEY = os.environ["AWS_ACCESS_KEY"]
        AWS_SECRET_KEY = os.environ["AWS_SECRET_KEY"]
        conn = S3Connection(AWS_ACCESS_KEY, AWS_SECRET_KEY)
        bucket = conn.get_bucket(BUCKET_NAME)
        k = Key(bucket)
        logger.info('Uploading %s to Amazon S3 bucket %s' % (fn, BUCKET_NAME))
        k.key = fn.replace('images/', '').replace('__', '/')
        k.set_contents_from_filename(fn)
    return filenames


@celery.task(name='celerytasks.crop_and_scale_file')
def crop_and_scale_file(filename):
    origIm = Image.open(filename)
    # crop Image from the top
    box = (0, 0, 1280, 1280)
    croppedIm = origIm.crop(box)
    croppedfilename = filename.replace('-full.png', '-top.jpg')
    croppedIm.save(croppedfilename)
    # resize cropped image
    newwidth = croppedIm.size[0] / 2
    newheight = croppedIm.size[1] / 2
    thumbIm = croppedIm.resize((newwidth, newheight), Image.ANTIALIAS)
    thumbfilename = filename.replace('-full.png', '-thumb.jpg')
    thumbIm.save(thumbfilename)
    # save origin as jpg, and remove png
    newfilename = filename.replace('.png', '.jpg')
    origIm.save(newfilename)
    os.remove(filename)
    return thumbfilename, croppedfilename, newfilename


@celery.task(name='celerytasks.fetch_webscreenshot')
def fetch_webscreenshot(url, dry_run=False):
    user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.8; rv:15.0) Gecko/20100101 Firefox/15.0.1'
    webkit2png_cmd = """./webkit2png --user-agent='{0}' -W 1280 -H 1280 -D images -F -o '{1}' {2}"""
    webkit2png_cmd += """ 2>&1 >/dev/null"""
    fileext = "-full.png"
    parsed = urlsplit(url)
    canonicalurl = parsed.netloc.lstrip('www.')
    urlpath = parsed.path.strip('/')
    if urlpath:
        canonicalurl += "|" + urlpath.replace('/', '|')
    now = datetime.datetime.now()
    filename = now.strftime("%Y__%m__%d") + "__" + canonicalurl + "__" + now.strftime("%H.%M")
    webkit2png_cmd = webkit2png_cmd.format(user_agent, filename, url)
    if dry_run:
        logger.info(webkit2png_cmd)
        return os.path.join("images", filename + fileext)
    ret = subprocess.call(webkit2png_cmd, shell=True)
    if ret != 0:
        raise IOError("unable to fetch '{0}', failed with return code {1}.".format(url, ret))
    return os.path.join("images", filename + fileext)


@celery.task(name='celerytasks.cleanup')
def cleanup():
    import glob
    for pngfile in glob.glob("images/*.png"):
        crop_and_scale_file(pngfile)
    jpegs = glob.glob("images/*.jpg")
    if jpegs:
        chain = (
            upload_files.s(jpegs) |
            remove_files.s()
        )
        chain()


@celery.task(name='celerytasks.webscreenshots')
def webscreenshots():
    for ws in WebSite.objects.all():
        chain = (
            fetch_webscreenshot.s(ws.url) |
            crop_and_scale_file.s()       |
            upload_files.s()              |
            remove_files.s()
        )
        chain()


if __name__ == '__main__':
#    cleanup()
    for ws in WebSite.objects.all():
        print fetch_webscreenshot(ws.url, dry_run=True)
    webscreenshots.delay()

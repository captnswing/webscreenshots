import datetime
import subprocess
from urlparse import urlsplit
import os
from PIL import Image, ImageFile
from celery.utils.log import get_task_logger
from boto.s3.connection import S3Connection
from boto.s3.key import Key
from webscreenshots.celeryapp import celery

os.environ["DJANGO_SETTINGS_MODULE"] = "webscreenshots.settings"
from webscreenshots.main.models import WebSite

logger = get_task_logger(__name__)
BUCKET_NAME = "svti-webscreenshots"
IMAGE_DIR = "/tmp"


@celery.task(name='webscreenshots.celerytasks.remove_files')
def remove_files(filenames):
    if isinstance(filenames, basestring):
        filenames = [filenames]
    for fn in filenames:
        os.remove(fn)


@celery.task(name='webscreenshots.celerytasks.upload_files')
def upload_files(filenames, boto_cfg=True):
    if isinstance(filenames, basestring):
        filenames = [filenames]
    for fn in filenames:
        if boto_cfg:
            # keys defined in /etc/boto.cfg
            conn = S3Connection()
        else:
            # keys defined in environment
            AWS_ACCESS_KEY = os.environ["AWS_ACCESS_KEY"]
            AWS_SECRET_KEY = os.environ["AWS_SECRET_KEY"]
            conn = S3Connection(AWS_ACCESS_KEY, AWS_SECRET_KEY)
        bucket = conn.get_bucket(BUCKET_NAME)
        k = Key(bucket)
        logger.info('Uploading %s to Amazon S3 bucket %s' % (fn, BUCKET_NAME))
        k.key = fn.replace(IMAGE_DIR + '/', '').replace('__', '/')
        k.set_contents_from_filename(fn)
    return filenames


def save_progressive_jpeg(im, filepath):
    # http://calendar.perfplanet.com/2012/progressive-jpegs-a-new-best-practice/
    logger.info('saving %s as progressive jpeg' % filepath)
    # from http://stackoverflow.com/a/6789306/41404
    try:
        im.save(filepath, "JPEG", quality=90, optimize=True, progressive=True)
    except IOError:
        ImageFile.MAXBLOCK = im.size[0] * im.size[1] * 2
        im.save(filepath, "JPEG", quality=90, optimize=True, progressive=True)


@celery.task(name='webscreenshots.celerytasks.crop_and_scale_file')
def crop_and_scale_file(filename):
    origIm = Image.open(filename)
    # crop Image from the top
    croppedIm = origIm.crop((0, 0, 1280, 1280))
    croppedfilename = filename.replace('.png', '-top.jpg')
    save_progressive_jpeg(croppedIm, croppedfilename)
    # resize cropped image
    thumbIm = croppedIm.resize((croppedIm.size[0]/2, croppedIm.size[1]/2), Image.ANTIALIAS)
    thumbfilename = filename.replace('.png', '-thumb.jpg')
    save_progressive_jpeg(thumbIm, thumbfilename)
    # save origin as .jpg
    origfilename = filename.replace('.png', '.jpg')
    save_progressive_jpeg(origIm, origfilename)
    # and remove the original .png
    os.remove(filename)
    return thumbfilename, croppedfilename, origfilename


def create_filename(url):
    parsed = urlsplit(url)
    canonicalurl = parsed.netloc.lstrip('www.')
    urlpath = parsed.path.strip('/')
    if urlpath:
        canonicalurl += "|" + urlpath.replace('/', '|')
    now = datetime.datetime.now()
    filename = now.strftime("%Y__%m__%d") + "__" + canonicalurl + "__" + now.strftime("%H.%M")
    return filename


@celery.task(name='webscreenshots.celerytasks.fetch_webscreenshot')
def fetch_webscreenshot(url, dry_run=False):
    filename = create_filename(url)
    # todo: take from localsettings
    phantomjs_bin = "/opt/phantomjs-1.7.0-linux-x86_64/bin/phantomjs"
    # todo: take from localsettings
    capture_script = "capture.js"
    phantomjs_cmd = "%s %s %s %s" % (phantomjs_bin, capture_script, url, "/tmp/%s.png" % filename.replace('|', '\|'))
    if dry_run:
        logger.info(phantomjs_cmd)
        return os.path.join(IMAGE_DIR, filename + ".png")
    logger.info('running phantomjs with url %s' % url)
    ret = subprocess.call(phantomjs_cmd, shell=True)
    if ret != 0:
        raise IOError("unable to fetch '{0}', failed with return code {1}.".format(url, ret))
    return os.path.join(IMAGE_DIR, filename + ".png")


@celery.task(name='webscreenshots.celerytasks.cleanup')
def cleanup():
    import glob
    for pngfile in glob.glob(IMAGE_DIR + "/*.png"):
        crop_and_scale_file(pngfile)
    jpegs = glob.glob(IMAGE_DIR + "/*.jpg")
    for fn in jpegs:
        chain = (
            upload_files.s(fn) |
            remove_files.s()
        )
        chain()


@celery.task(name='webscreenshots.celerytasks.webscreenshots')
def webscreenshots():
    for ws in WebSite.objects.all():
        chain = (
            fetch_webscreenshot.s(ws.url) |
            crop_and_scale_file.s() |
            upload_files.s() |
            remove_files.s()
        )
        chain()


if __name__ == '__main__':
    cleanup()

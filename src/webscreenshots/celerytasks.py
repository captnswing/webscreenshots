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
        # logger.info("removing %s" % fn)
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


@celery.task(name='webscreenshots.celerytasks.crop_and_scale_file')
def crop_and_scale_file(filename):
    origIm = Image.open(filename)
    # crop Image from the top
    box = (0, 0, 1280, 1280)
    croppedIm = origIm.crop(box)
    # croppedfilename = filename.replace('-full.png', '-top.jpg')
    croppedfilename = filename.replace('.png', '-top.jpg')
    # from http://stackoverflow.com/a/6789306/41404
    ImageFile.MAXBLOCK = croppedIm.size[0] * croppedIm.size[1]
    logger.info('saving croppedfile %s' % croppedfilename)
    croppedIm.save(croppedfilename, quality=90, optimize=True, progressive=True)
    # resize cropped image
    newwidth = croppedIm.size[0] / 2
    newheight = croppedIm.size[1] / 2
    thumbIm = croppedIm.resize((newwidth, newheight), Image.ANTIALIAS)
    thumbfilename = filename.replace('.png', '-thumb.jpg')
    # from http://stackoverflow.com/a/6789306/41404
    ImageFile.MAXBLOCK = thumbIm.size[0] * thumbIm.size[1]
    logger.info('saving thumbfile %s' % thumbfilename)
    thumbIm.save(thumbfilename, quality=90, optimize=True, progressive=True)
    # save origin as jpg, and remove png
    newfilename = filename.replace('.png', '.jpg')
    # from http://stackoverflow.com/a/6789306/41404
    ImageFile.MAXBLOCK = origIm.size[0] * origIm.size[1]
    logger.info('saving newfile %s' % newfilename)
    origIm.save(newfilename, quality=90, optimize=True, progressive=True)
    try:
        os.remove(filename)
    except OSError:
        pass
    return thumbfilename, croppedfilename, newfilename


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
    js_tmpl = """
    var pageurl = '%s';
    var pagepng = '%s';
    var page = require('webpage').create();
    page.viewportSize = { width: 1280, height: 720 };
    page.open(pageurl, function (status) {
        if (status !== 'success') {
            console.log('Unable to access the network!');
        } else {
            page.evaluate(function () {
                var body = document.body;
                body.style.backgroundColor = '#fff';
            });
            page.render(pagepng);
        }
        phantom.exit();
    });
    """
    filename = create_filename(url)
    phantomjs_cmd = "/opt/phantomjs-1.7.0-linux-x86_64/bin/phantomjs /tmp/%s.js" % filename.replace('|', '\|')
    if dry_run:
        logger.info(js_tmpl % (url, filename + ".png"))
        logger.info(phantomjs_cmd)
        return os.path.join(IMAGE_DIR, filename + ".png")
    jsfile = open("/tmp/%s.js" % filename, 'w')
    jsfile.write(js_tmpl % (url, IMAGE_DIR+ "/" + filename + ".png"))
    jsfile.close()
    logger.info('running phantomjs /tmp/%s.js' % filename)
    ret = subprocess.call(phantomjs_cmd, shell=True)
    if ret != 0:
        raise IOError("unable to fetch '{0}', failed with return code {1}.".format(url, ret))
    os.remove("/tmp/%s.js" % filename)
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
    for ws in WebSite.objects.all():
        print fetch_webscreenshot(ws.url, dry_run=True)

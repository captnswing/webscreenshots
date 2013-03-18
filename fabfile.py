#!/usr/bin/env python
#-*- coding: utf-8 -*-
from fabric.api import cd, prefix, run, env, shell_env, task, local, get, prompt
import datetime
from boto.s3.connection import S3Connection
import os
from webscreenshots.main.models import WebSite

env.hosts = ['ec2-54-228-243-189.eu-west-1.compute.amazonaws.com']
env.activate = 'source /opt/webscreenshots/bin/activate'
env.directory = '/opt/webscreenshots/src/webscreenshots/src/webscreenshots'
env.shell_env = {'DJANGO_SETTINGS_MODULE': 'webscreenshots.settings.prod'}
env.use_ssh_config = True


def get_env_variable(var_name):
    """ Get the environment variable or return exception """
    try:
        return os.environ[var_name]
    except KeyError:
        raise ValueError("Set the %s env variable" % var_name)


@task
def dbdump():
    DUMPAPPS = 'auth contenttypes admin main statistics'
    with cd(env.directory), shell_env(**env.shell_env), prefix(env.activate):
        run("./manage.py dumpdata --indent=4 %s >/tmp/dbbackup_%s.json" % (DUMPAPPS, datetime.datetime.today().strftime("%Y-%m-%d")))
        run("gzip /tmp/dbbackup_%s.json" % datetime.datetime.today().strftime("%Y-%m-%d"))
        get("/tmp/dbbackup_%s.json.gz" % datetime.datetime.today().strftime("%Y-%m-%d"), local_path="src/webscreenshots/main/fixtures")


@task
def fetch_celeryd_logs():
    local('rsync --times --progress --compress --rsh=/usr/bin/ssh ec2-54-228-243-189.eu-west-1.compute.amazonaws.com:/opt/webscreenshots/var/log/celeryd.log\* celerylogs')
    #get('/opt/webscreenshots/var/log/celeryd.log*')


@task
def remove_site_from_se(sitetoremove=None):
    AWS_ACCESS_KEY = get_env_variable("AWS_ACCESS_KEY")
    AWS_SECRET_KEY = get_env_variable("AWS_SECRET_KEY")
    if not sitetoremove:
        sitetuple = list(enumerate(WebSite.objects.all()))
        nrrange = zip(*sitetuple)[0]
        for i, s in sitetuple:
            print "{0:>2}) {1}".format(i+1, s)

    def choiceinrange(input):
        try:
            input = int(input)
        except:
            raise ValueError("invalid choice '%s'" % input)

        if int(input)-1 in nrrange:
            return int(input)
        else:
            raise ValueError("invalid choice '%s'" % input)

    sitenr = prompt("choose site nr: ", validate=choiceinrange)
    sitetoremove = sitetuple[sitenr-1][1]
    yes = prompt("really delete all occurences of '%s' (y/n)?" % sitetoremove, validate=lambda x: x.lower() == 'y')
    if not yes:
        print "mission aborted."
        return
    conn = S3Connection(AWS_ACCESS_KEY, AWS_SECRET_KEY)
    bucket = conn.get_bucket("svti-webscreenshots")
    d = datetime.datetime(2013, 1, 4)
    delta = datetime.timedelta(days=1)
    while d <= datetime.datetime.today():
        path = "%s/%s" % (d.strftime("%Y/%m/%d"), sitetoremove)
        print path
        bucketListResultSet = bucket.list(prefix=path)
        _result = bucket.delete_keys([key.name for key in bucketListResultSet])
        d += delta

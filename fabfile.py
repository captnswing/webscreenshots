#!/usr/bin/env python
#-*- coding: utf-8 -*-
from fabric.api import cd, prefix, run, env, shell_env, task, local, get
import datetime
from boto.s3.connection import S3Connection
import os

env.hosts = ['ec2-54-228-243-189.eu-west-1.compute.amazonaws.com']
env.activate = 'source /opt/webscreenshots/bin/activate'
env.directory = '/opt/webscreenshots/src/webscreenshots/src/webscreenshots'
env.shell_env = {'DJANGO_SETTINGS_MODULE': 'webscreenshots.settings.prod'}
env.use_ssh_config = True


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
def remove_site_from_se(sitetoremove):
    AWS_ACCESS_KEY = os.environ["AWS_ACCESS_KEY"]
    AWS_SECRET_KEY = os.environ["AWS_SECRET_KEY"]
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

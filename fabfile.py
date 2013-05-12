#!/usr/bin/env python
#-*- coding: utf-8 -*-
from fabric.api import cd, prefix, run, env, shell_env, task, local, get, prompt
import datetime
from boto.s3.connection import S3Connection
import os
from webscreenshots.main.models import WebSite

env.use_ssh_config = True
#env.disable_known_hosts = True


def get_env_variable(var_name):
    """ Get the environment variable or return exception """
    try:
        return os.environ[var_name]
    except KeyError:
        raise ValueError("Set the %s env variable" % var_name)

@task
def prod():
    env.hosts = ['webscreenshots.captnswing.net']
    env.activate = 'source /opt/webscreenshots/bin/activate'
    env.directory = '/opt/webscreenshots/src/webscreenshots/src/webscreenshots'
    env.shell_env = {'DJANGO_SETTINGS_MODULE': 'webscreenshots.settings.prod'}

@task
def test():
    env.hosts = ['test.webscreenshots.captnswing.net']
    env.activate = 'source /opt/webscreenshots/bin/activate'
    env.directory = '/opt/webscreenshots/src/webscreenshots/src/webscreenshots'
    env.shell_env = {'DJANGO_SETTINGS_MODULE': 'webscreenshots.settings.test'}

@task
def dev():
    env.hosts = ['ec2-54-228-34-186.eu-west-1.compute.amazonaws.com']
    env.activate = 'source /opt/webscreenshots/bin/activate'
    env.directory = '/opt/webscreenshots/src/webscreenshots/src/webscreenshots'
    env.shell_env = {'DJANGO_SETTINGS_MODULE': 'webscreenshots.settings.test'}

@task
def deploy():
    with cd(env.directory), shell_env(**env.shell_env), prefix(env.activate):
        run("cd ..; hg pull; hg update")

@task
def dbdump():
    DUMPAPPS = 'auth admin main statistics'
    with cd(env.directory), shell_env(**env.shell_env), prefix(env.activate):
        run("./manage.py dumpdata --indent=4 %s >/tmp/dbbackup_%s.json" % (DUMPAPPS, datetime.datetime.today().strftime("%Y-%m-%d")))
        run("gzip /tmp/dbbackup_%s.json" % datetime.datetime.today().strftime("%Y-%m-%d"))
        get("/tmp/dbbackup_%s.json.gz" % datetime.datetime.today().strftime("%Y-%m-%d"), local_path="src/webscreenshots/main/fixtures")
        print "downloaded dbbackup_%s.json.gz to 'src/webscreenshots/main/fixtures'" % datetime.datetime.today().strftime("%Y-%m-%d")

@task
def fetch_celeryd_logs():
    local('rsync --times --progress --compress --rsh=/usr/bin/ssh ec2-54-228-243-189.eu-west-1.compute.amazonaws.com:/opt/webscreenshots/var/log/celeryd.log\* celerylogs')
    #get('/opt/webscreenshots/var/log/celeryd.log*')

@task
def rsync_code():
    excludes = [".idea", ".hg*", ".vagrant", "build", "dist", "setuptools*", "webscreenshots_kitchen", "distribute*", "celerylogs", "src/webscreenshots.egg-info"]
    excludes = [ "--exclude=\"{0}\"".format(e) for e in excludes ]
    excludes = " ".join(excludes)
    rsync_options = "--progress --compress --rsh=/usr/bin/ssh --recursive --times --perms --links {0}".format(excludes)
    rsync_cmd = "rsync {0} . {1}:/opt/webscreenshots/src/webscreenshots/".format(rsync_options, env.hosts[0])
    local(rsync_cmd)
    run("touch %s/wsgi.py" % env.directory)

@task
def remove_site_from_s3(sitetoremove=None):
    AWS_ACCESS_KEY = get_env_variable("AWS_ACCESS_KEY")
    AWS_SECRET_KEY = get_env_variable("AWS_SECRET_KEY")
    if not sitetoremove:
        sitetuple = list(enumerate(WebSite.objects.all()))
        nrrange = zip(*sitetuple)[0]
        for i, s in sitetuple:
            print "{0:>2}) {1}".format(i+1, s)

    def choiceinrange(userinput):
        try:
            userinput = int(userinput)
        except:
            raise ValueError("invalid choice '%s'" % userinput)

        if int(userinput)-1 in nrrange:
            return int(userinput)
        else:
            raise ValueError("invalid choice '%s'" % userinput)

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

#!/usr/bin/env python
#-*- coding: utf-8 -*-
from fabric.api import cd, prefix, run, env, shell_env, task, local


env.hosts = ['ec2-54-228-243-189.eu-west-1.compute.amazonaws.com']
env.activate = 'source /opt/webscreenshots/bin/activate'
env.directory = '/opt/webscreenshots/src/webscreenshots/src/webscreenshots'
env.shell_env = {'DJANGO_SETTINGS_MODULE': 'webscreenshots.settings.prod'}
env.use_ssh_config = True


@task
def dbdump():
    with cd(env.directory), shell_env(**env.shell_env), prefix(env.activate):
        run("./manage.py dumpdata --indent=4 main")


@task
def fetch_celeryd_logs():
    local('rsync --times --progress --compress --rsh=/usr/bin/ssh ec2-54-228-243-189.eu-west-1.compute.amazonaws.com:/opt/webscreenshots/var/log/celeryd.log\* celerylogs')
    #get('/opt/webscreenshots/var/log/celeryd.log*')

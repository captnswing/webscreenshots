#!/usr/bin/env python
#-*- coding: utf-8 -*-
from fabric.api import cd, prefix, run, env, shell_env, get
from collections import defaultdict
import re
import datetime
import gzip
import bz2

env.hosts = ['ec2-54-228-243-189.eu-west-1.compute.amazonaws.com']
env.activate = 'source /opt/webscreenshots/bin/activate'
env.directory = '/opt/webscreenshots/src/webscreenshots/src/webscreenshots'
env.djangosettings = 'webscreenshots.settings.prod'
env.use_ssh_config = True


def dbdump():
    with cd(env.directory), shell_env(DJANGO_SETTINGS_MODULE=env.djangosettings), prefix(env.activate):
        run("./manage.py dumpdata --indent=4 main")


def fetch_celeryd_logs():
    get('/opt/webscreenshots/var/log/celeryd.log*')


# http://www.dabeaz.com/generators/Generators.pdf
def gen_find(filepat, top):
    import os, fnmatch
    for path, dirlist, filelist in os.walk(top):
        for name in fnmatch.filter(filelist, filepat):
            yield os.path.join(path, name)


# http://www.dabeaz.com/generators/Generators.pdf
def gen_open(filenames):
    for name in filenames:
        if name.endswith(".gz"):
            yield gzip.open(name)
        elif name.endswith(".bz2"):
            yield bz2.BZ2File(name)
        else:
            yield open(name)


# http://www.dabeaz.com/generators/Generators.pdf
def gen_cat(sources):
    for s in sources:
        for item in s:
            yield item


# http://www.dabeaz.com/generators/Generators.pdf
def gen_grep(pat, lines):
    patc = re.compile(pat)
    for line in lines:
        if patc.search(line):
            yield line


def get_starts(logfilematch, logdir):
    start_pattern = re.compile(r".*\[(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}).*Got task from broker: webscreenshots.celerytasks.fetch_webscreenshot.*\[(.*?)\]")
    lognames = gen_find(logfilematch, logdir)
    logfiles = gen_open(lognames)
    loglines = gen_cat(logfiles)
    groups = (start_pattern.match(line) for line in loglines)
    tuples = (g.groups() for g in groups if g)
    parsed_tuples = ((b, datetime.datetime.strptime(a, "%Y-%m-%d %H:%M:%S")) for a,b in tuples)
    # parsed_tuples = ((b, a) for a,b in tuples)
    return parsed_tuples


def get_ends(logfilematch, logdir):
    end_pattern = re.compile(r".*\[(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}).*Task webscreenshots.celerytasks.fetch_webscreenshot\[(.*?)\] succeeded in (\d+.\d+)?.*")
    lognames = gen_find(logfilematch, logdir)
    logfiles = gen_open(lognames)
    loglines = gen_cat(logfiles)
    groups = (end_pattern.match(line) for line in loglines)
    tuples = (g.groups() for g in groups if g)
    parsed_tuples = ((b, datetime.datetime.strptime(a, "%Y-%m-%d %H:%M:%S"), c) for a,b,c in tuples)
    return parsed_tuples


def process_logs():
    logfilematch = "celeryd.log.4*"
    logdir = "ec2-54-228-243-189.eu-west-1.compute.amazonaws.com"
    screenshots = defaultdict(dict)

    parsed_tuples = get_starts(logfilematch, logdir)
    # print len(list(parsed_tuples))
    for sid, start in parsed_tuples:
        screenshots[sid].update({
            'start': start
        })

    parsed_tuples = get_ends(logfilematch, logdir)
    # print len(list(parsed_tuples))
    for sid, end, duration in parsed_tuples:
        screenshots[sid].update({
            'end': end,
            'duration': duration
        })

    complete = list()
    for sc in screenshots:
        if set(screenshots[sc].keys()).issuperset({'start', 'end', 'duration'}):
            complete.append(screenshots[sc])
    print len(complete)
    durations = [float(l['duration']) for l in complete]
    print "Average duration %.2fsec" % (sum(durations)/len(durations))
    starttimes = [l['end'].strftime("%H:%M:%S") for l in complete]
    print starttimes


if __name__ == '__main__':
    process_logs()

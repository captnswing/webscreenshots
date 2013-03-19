#-*- coding: utf-8 -*-
from django.http import HttpResponse
from collections import defaultdict, Counter
from django.shortcuts import render_to_response
from django.template.context import RequestContext
import json
import re
import gzip
import bz2
import datetime
from django.conf import settings


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


def get_celery_loglines(fnmatch="celeryd.log*", logdir=settings.CELERYD_LOGPATH):
    lognames = gen_find(fnmatch, logdir)
    logfiles = gen_open(lognames)
    loglines = gen_cat(logfiles)
    return loglines


def loglines_for_date(chosendate=datetime.datetime.today()):
    chosendate = chosendate.strftime("%Y-%m-%d")
    loglines = get_celery_loglines()
    loglines = (l for l in loglines if l[1:11] == chosendate)
    return loglines


def get_starts(chosendate=datetime.datetime.today()):
    start_pattern = re.compile(r".*\[(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}).*Got task from broker: webscreenshots.celerytasks.fetch_webscreenshot.*\[(.*?)\]")
    loglines = loglines_for_date(chosendate)
    groups = (start_pattern.match(line) for line in loglines)
    tuples = (g.groups() for g in groups if g)
    parsed_tuples = ((b, datetime.datetime.strptime(a, "%Y-%m-%d %H:%M:%S")) for a, b in tuples)
    return parsed_tuples


def get_ends(chosendate=datetime.datetime.today()):
    end_pattern = re.compile(r".*\[(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}).*Task webscreenshots.celerytasks.fetch_webscreenshot\[(.*?)\] succeeded in (\d+.\d+)?.*/tmp/\d{4}__\d{2}__\d{2}__(.*)")
    loglines = loglines_for_date(chosendate)
    groups = (end_pattern.match(line) for line in loglines)
    tuples = (g.groups() for g in groups if g)
    parsed_tuples = ((b, datetime.datetime.strptime(a, "%Y-%m-%d %H:%M:%S"), c, d.replace('|', '/')) for a, b, c, d in tuples)
    return parsed_tuples


def main(request, statdate=None):
    today = datetime.datetime.today()
    if not statdate:
        statdate = today
    else:
        statdate = datetime.datetime.strptime(statdate, "%Y-%m-%d")

    screenshots = defaultdict(dict)
    for sid, start in get_starts(statdate):
        screenshots[sid].update({
            'start': start
        })
    for sid, end, duration, site in get_ends(statdate):
        screenshots[sid].update({
            'end': end,
            'duration': duration,
            'site': site
        })

    complete = list()
    for sc in screenshots:
        if set(screenshots[sc].keys()).issuperset({'start', 'end', 'duration', 'site'}):
            complete.append(screenshots[sc])
    durations = [round(float(l['duration']), 0) for l in complete]
    average = sum(durations)/len(durations)
    cnt = Counter(durations)
    histogram = list()
    for k in sorted(cnt.keys()):
        histogram.append([int(k), cnt[k]])

    histdata = [ (i,j) for i,j in histogram if i <= 300]
    longjobs = [ (i,j) for i,j in histogram if i  > 60]

    longjobs_percent = 0
    if len(complete):
        longjobs_percent = float(len(longjobs))/len(complete)*100

    return render_to_response('statistics.html', {
        'statdate': statdate,
        'histdata': json.dumps(histdata),
        'number_of_jobs': len(complete),
        'average_duration': average,
        'longjobs': len(longjobs),
        'longjobs_percent': longjobs_percent
    }, context_instance=RequestContext(request))


if __name__ == '__main__':
    for l in get_ends(datetime.datetime(2013,03,16)):
        print l

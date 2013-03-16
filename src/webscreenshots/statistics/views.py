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


def get_starts(logfilematch, logdir):
    start_pattern = re.compile(r".*\[(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}).*Got task from broker: webscreenshots.celerytasks.fetch_webscreenshot.*\[(.*?)\]")
    lognames = gen_find(logfilematch, logdir)
    logfiles = gen_open(lognames)
    loglines = gen_cat(logfiles)
    groups = (start_pattern.match(line) for line in loglines)
    tuples = (g.groups() for g in groups if g)
    parsed_tuples = ((b, datetime.datetime.strptime(a, "%Y-%m-%d %H:%M:%S")) for a, b in tuples)
    return parsed_tuples


def get_ends(logfilematch, logdir):
    end_pattern = re.compile(r".*\[(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}).*Task webscreenshots.celerytasks.fetch_webscreenshot\[(.*?)\] succeeded in (\d+.\d+)?.*/tmp/\d{4}__\d{2}__\d{2}__(.*)")
    lognames = gen_find(logfilematch, logdir)
    logfiles = gen_open(lognames)
    loglines = gen_cat(logfiles)
    groups = (end_pattern.match(line) for line in loglines)
    tuples = (g.groups() for g in groups if g)
    parsed_tuples = ((b, datetime.datetime.strptime(a, "%Y-%m-%d %H:%M:%S"), c, d.replace('|', '/')) for a, b, c, d in tuples)
    return parsed_tuples


def main(request):
    return render_to_response('statistics.html', {
    }, context_instance=RequestContext(request))


def histdata(request):
    logfilematch = "celeryd.log"
    screenshots = defaultdict(dict)

    parsed_tuples = get_starts(logfilematch, settings.CELERYD_LOGPATH)
    for sid, start in parsed_tuples:
        screenshots[sid].update({
            'start': start
        })

    parsed_tuples = get_ends(logfilematch, settings.CELERYD_LOGPATH)
    for sid, end, duration, site in parsed_tuples:
        screenshots[sid].update({
            'end': end,
            'duration': duration,
            'site': site
        })

    complete = list()
    for sc in screenshots:
        if set(screenshots[sc].keys()).issuperset({'start', 'end', 'duration', 'site'}):
            complete.append(screenshots[sc])
    print "Number of jobs: %s" % len(complete)
    durations = [round(float(l['duration']), 0) for l in complete]
    print "Average duration: %.2fsec" % (sum(durations)/len(durations))
    cnt = Counter(durations)
    histogram = list()
    for k in sorted(cnt.keys()):
        histogram.append([int(k), cnt[k]])
    return HttpResponse(json.dumps(histogram[:100]), mimetype="application/json")

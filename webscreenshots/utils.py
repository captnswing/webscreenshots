#!/usr/bin/env python
# -*- coding: utf-8 -*-
from webscreenshots.celeryapp import celery
import collections
import datetime
import unittest


def calculate_expexted_times():
    celery_schedule = celery.conf['CELERYBEAT_SCHEDULE']
    cronentries = [celery_schedule[schedule_entry]['schedule'] for schedule_entry in celery_schedule]
    expected_times = list()
    for c in cronentries:
        expected_times += ["{0:>02}.{1:>02}".format(h, m) for h in c.hour for m in c.minute]
    expected_times = sorted(expected_times)
    return expected_times


# from http://stackoverflow.com/a/10854034/41404
def roundTime(dt, roundTo=5 * 60):
    """Round a datetime object to any time laps in seconds
    dt : datetime.datetime object, default now.
    roundTo : Closest number of seconds to round to, default 5 minutes.
    """
    seconds = (dt - dt.min).seconds
    # '//' is a floor division, not a comment on following line:
    rounding = (seconds + roundTo / 2) // roundTo * roundTo
    return dt + datetime.timedelta(0, rounding - seconds, -dt.microsecond)


def get_slice_from_list(mylist, idx, siblings=2):
    s_start = idx - siblings
    s_stop = idx + siblings + 1
    if s_start < 0:
        # http://pymotw.com/2/collections/deque.html#rotating
        mylist = collections.deque(mylist)
        mylist.rotate(-1 * s_start)
        mylist = list(mylist)
        return mylist[0:(siblings * 2 + 1)]
    elif s_stop >= len(mylist):
        # http://pymotw.com/2/collections/deque.html#rotating
        mylist = collections.deque(mylist)
        mylist.rotate(len(mylist) - s_stop)
        mylist = list(mylist)
        return mylist[-(siblings * 2 + 1):]
    else:
        return mylist[s_start:s_stop]


if __name__ == '__main__':
    unittest.main()

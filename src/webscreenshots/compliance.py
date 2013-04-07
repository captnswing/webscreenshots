#!/usr/bin/env python
#-*- coding: utf-8 -*-
from webscreenshots.celeryapp import celery


def get_expected_times():
    celery_schedule = celery.conf['CELERYBEAT_SCHEDULE']
    cronentries = [celery_schedule[schedule_entry]['schedule'] for schedule_entry in celery_schedule]
    expected_times = list()
    for c in cronentries:
        expected_times += ["{0:>02}.{1:>02}".format(h, m) for h in c.hour for m in c.minute]
    expected_times = sorted(expected_times)
    return expected_times


def main():
    et = get_expected_times()
    print et


if __name__ == '__main__':
    main()

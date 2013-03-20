from __future__ import absolute_import
from celery import Celery
from celery.schedules import crontab

celery = Celery('proj.celery',
    broker='redis://',
    backend='redis://',
)

# Optional configuration, see the application user guide.
celery.conf.update(
    CELERY_TIMEZONE = 'Europe/Stockholm',
    CELERY_IMPORTS='webscreenshots.celerytasks',
    CELERY_DISABLE_RATE_LIMITS = True,
    CELERY_TASK_RESULT_EXPIRES=3600,
    BROKER_TRANSPORT_OPTIONS={'visibility_timeout': 3600},
    # http://docs.celeryproject.org/en/latest/userguide/periodic-tasks.html#crontab-schedules
    CELERYBEAT_SCHEDULE = {
        'runs-every-5-minutes': {
            'task': 'webscreenshots.celerytasks.webscreenshots',
            'schedule': crontab(minute='*/5', hour='7-22'),
#            'schedule': crontab(minute='*/5'),
           },
        'runs-every-hour': {
            'task': 'webscreenshots.celerytasks.webscreenshots',
            'schedule': crontab(minute='0', hour='23-6'),
        }
    }
)


if __name__ == '__main__':
    celery.start()

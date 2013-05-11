from celery import Celery
from celery.schedules import crontab


celery = Celery(
    broker='redis://',
    backend='redis://',
)


# Optional configuration, see the application user guide.
celery.conf.update(
    CELERY_TIMEZONE='Europe/Stockholm',
    CELERY_IMPORTS='webscreenshots.celerytasks',
    CELERY_DISABLE_RATE_LIMITS=True,
    CELERY_TASK_RESULT_EXPIRES=3600,
    BROKER_TRANSPORT_OPTIONS={'visibility_timeout': 3600},
    # http://stackoverflow.com/a/10756040/41404
    # CELERY_ROUTES={
    #     "webscreenshots.celerytasks.webscreenshots": {"queue": "phantomjs"},
    #     "webscreenshots.celerytasks.fetch_webscreenshot": {"queue": "phantomjs"}
    # },
    # http://docs.celeryproject.org/en/latest/userguide/periodic-tasks.html#crontab-schedules
    CELERYBEAT_SCHEDULE={
        'runs-every-5-minutes': {
            'task': 'webscreenshots.celerytasks.webscreenshots',
            'schedule': crontab(minute='*/5', hour='7-22'),
        },
        'runs-every-hour': {
            'task': 'webscreenshots.celerytasks.webscreenshots',
            'schedule': crontab(minute='0', hour='23-6'),
        }
    }
)

if __name__ == '__main__':
    celery.start()

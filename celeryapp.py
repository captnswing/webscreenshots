from __future__ import absolute_import
from datetime import timedelta
from celery import Celery

celery = Celery('proj.celery',
    broker='redis://',
    backend='redis://',
)

# Optional configuration, see the application user guide.
celery.conf.update(
    CELERY_IMPORTS='celerytasks',
    CELERY_DISABLE_RATE_LIMITS = True,
    CELERY_TASK_RESULT_EXPIRES=3600,
    BROKER_TRANSPORT_OPTIONS={'visibility_timeout': 3600},
    CELERYBEAT_SCHEDULE = {
        'runs-every-5-minutes': {
            'task': 'celerytasks.webscreenshots',
            'schedule': timedelta(seconds=300),
        },
    }
)


CELERY_TIMEZONE = 'UTC'

if __name__ == '__main__':
    celery.start()

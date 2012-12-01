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
#    CELERYBEAT_SCHEDULE = {
#        'runs-every-6-seconds': {
#            'task': 'celerytasks.add',
#            'schedule': timedelta(seconds=6),
#            'args': (16, 16)
#        },
#    }
)


CELERY_TIMEZONE = 'UTC'

if __name__ == '__main__':
    celery.start()

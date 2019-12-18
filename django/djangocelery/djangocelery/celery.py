from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'djangocelery.settings')

app = Celery('djangocelery',
             #broker='amqp://',
             #backend='amqp://',
            )

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()

#@app.task(bind=True)
@app.task
def add(x, y):
    print("{} + {} = {}".format(x, y, x+y))
    return (x+y)

from time import sleep
from celery.contrib.abortable import AbortableTask

from celery.signals import worker_shutting_down

@worker_shutting_down.connect
def worker_shutting_down_handler(sig, how, exitcode, ** kwargs):
    print(f'worker_shutting_down({sig}, {how}, {exitcode})')

@app.task(bind=True, base=AbortableTask)
def longtask(self):
    from celery.platforms import signals
    from celery.contrib.abortable import AbortableAsyncResult

    def int_handler(signum, frame):
        id = self.request.id
        print(f'int_handler({signum}, {frame})')
        print(f'id = {id}')
        result = AbortableAsyncResult(id)
        result.abort()

    signals['INT'] = int_handler
    signals['TERM'] = int_handler

    for i in range(0, 4):
        if self.is_aborted():
            return 'aborted'
        print('sleeping 3 seconds')
        sleep(3)
    return 'completed'

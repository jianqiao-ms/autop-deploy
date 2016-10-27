#!/usr/bin/env python2
# -*- coding:UTF-8 -*-

from __future__ import absolute_import
from celery import Celery

App = Celery('worker',
             include=[
                 'worker.db',
                 'worker.tasks-new',
                 'worker.tasks-del'
             ])
App.config_from_object('celeryconf')

# Optional configuration, see the application user guide.
# App.conf.update(
#     CELERY_TASK_RESULT_EXPIRES=3600,
# )

if __name__ == '__main__':
    App.start()
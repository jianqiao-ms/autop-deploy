#!/usr/bin/env python2
# -*- coding:UTF-8 -*-

from __future__ import absolute_import
from celery import Celery

app = Celery('proj',
             include=[
                 'proj.db',
                 'proj.tasks_new',
                 'proj.tasks_del',
                 'proj.tasks_ucd'
             ])
app.config_from_object('proj._celeryconf')

# Optional configuration, see the application user guide.
app.conf.update(
    CELERY_TASK_RESULT_EXPIRES=3600,
)

if __name__ == '__main__':
    app.start()
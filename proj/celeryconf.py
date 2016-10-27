#!/usr/bin/env python2.7
# -*- coding:UTF-8 -*-

# BROKER_URL                  = 'redis://localhost:6379/0'
# CELERY_RESULT_BACKEND       = 'redis://localhost:6379/1'
BROKER_URL                  = 'amqp://celeryadmin:jianqiaoA1@localhost:5672/celery'
CELERY_RESULT_BACKEND       = 'amqp'

CELERY_TASK_SERIALIZER      = 'json'
CELERY_RESULT_SERIALIZER    = 'json'
CELERY_ACCEPT_CONTENT       = ['json']
CELERY_TIMEZONE             = 'Asia/Shanghai'
CELERY_ENABLE_UTC           = True
CELERYD_LOG_COLOR           = False


CELERY_ROUTES = {
    # 'tasks.add': 'low-priority',
}

CELERY_ANNOTATIONS = {
    # 'tasks.add': {'rate_limit': '10/m'}
}
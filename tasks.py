#!/usr/bin/env python2
# -*- coding:UTF-8 -*-

import torndb
from celery import Celery

celery = Celery("task")
celery.config_from_object('celeryconf')

db = torndb.Connection(host="192.168.0.195",database="autop",user='cupid',password='everyone2xhfz')

@celery.task
def mysql_query(cmd):
    return db.query(cmd)
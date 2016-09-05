#!/usr/bin/env python2
# -*- coding:UTF-8 -*-

import torndb
from celery import Celery

import subprocess
import time

celery = Celery("task")
celery.config_from_object('celeryconf')

db = torndb.Connection(host="192.168.0.195",database="autop",user='cupid',password='everyone2xhfz')

@celery.task
def mysql_query(cmd):
    return db.query(cmd)
@celery.task
def mysql_get(cmd):
    return db.query(cmd)
@celery.task
def deploy(pname):
    name_path = {'imanager_bi'      : 'imanager_bi',
                 'imanager_web'     : 'imanager_web',
                 'imanager_api'     : 'imanager_api',
                 'imanager_core'    : 'imanager',
                 'imanager_iclock'  : 'imanager_iclock',
                 'imanager_iservice': 'iservice',
                 'iservice'         : 'iservice',
                 'tf-oa'            : 'tf-oa',
                 'ApiForApp'        : 'ApiForApp'
                 }

    # 切换目录
    cmd = "cd /var/run/autop/repo/{path}".format(path = name_path[pname])
    a = subprocess.check_output(cmd,shell=True)
    return a

@celery.task
def sleep(n):
    time.sleep(5)
    return 0
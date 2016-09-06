#!/usr/bin/env python2
# -*- coding:UTF-8 -*-

import torndb
from celery import Celery

import os
import time
import subprocess

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
                 'oa'               : 'oa'
                 }

    name_host = {'imanager_bi'      : ['192.168.0.101'],
                 'imanager_web'     : ['192.168.0.105'],
                 'imanager_api'     : ['192.168.0.126'],
                 'imanager_core'    : ['ALL'],
                 'imanager_iclock'  : ['192.168.0.81'],
                 'imanager_iservice': ['192.168.0.112','192.168.0.111'],
                 'iservice'         : ['192.168.0.150', '192.168.0.151', '192.168.0.152', '192.168.0.153', '192.168.0.154',],
                 'oa'               : ['192.168.0.91']
                 }

    msg  = list()
    flag = None

    # 切换目录
    msg.append('[OK]检测项目repo')
    path = "/var/autop/repo/{path}".format(path = name_path[pname])
    if os.path.isdir(path):
        os.chdir(path)
        msg.append('[OK]项目repo 存在')
        msg.append('[OK]切换到项目repo {path}'.format(path = path))
    else:
        msg.append('[WARNNING]项目repo 不存在，初始化项目')
        os.chdir('/var/autop/repo')
        r = subprocess.check_call('git clone git@192.168.1.141:devs/{}.git'.format(pname))
        if r == 0:
            msg.append('[OK]项目初始化成功')
            os.chdir(path)
            flag = 'newInit'


    # 更新项目
    a = subprocess.check_output(cmd,shell=True)
    time.sleep(10)
    return a


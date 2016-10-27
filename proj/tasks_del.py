#!/usr/bin/env python2
# -*- coding:UTF-8 -*-

# celery App 子模块必须引入的包
from __future__ import absolute_import
from proj.celery import App
from proj.db import db_conn

# 异常
from torndb import IntegrityError
from socket import gaierror

# 功能性import
import traceback
import os

@App.task
def del_autorule(arid):
    try:
        sql = 'SELECT alias FROM `t_assets_project` p LEFT JOIN `t_deploy_auto_rule` ar ON ar.project_id=p.id WHERE ar.id={}'.format(arid)
        pAlias = db_conn.get(sql)['alias']
        pPath = '/var/autop/repo/{}___master'.format(pAlias)
        if os.path.exists(pPath):
            os.system('rm -rf {}'.format(pPath))
        sql = "DELETE FROM `t_deploy_auto_rule` WHERE id={}".format(arid)
        db_conn.delete(sql)
        return dict(code=0)
    except IntegrityError as e:
        return dict(code=11, column=e.args[1].split()[-1][1:-1])
    except Exception as e:
        return dict(type=type(e).__name__, info=traceback.format_exc(), code=400)
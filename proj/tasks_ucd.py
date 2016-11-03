#!/usr/bin/env python2
# -*- coding:UTF-8 -*-

# ucd
# u - update
# c - compile
# d - deploy

# celery app 子模块必须引入的包
from __future__ import print_function
from __future__ import print_function
from __future__ import absolute_import
from proj.celery import app
from proj.db import mysql_insert
from proj.db import mysql_delete
from proj.db import mysql_update
from proj.db import mysql_query
from proj.db import mysql_get

# 异常
from torndb import IntegrityError

# 系统包
import re
import os
import sys
import time
import traceback
import subprocess

# Description of return code
#
# 0 : OK
# 1 : 分支不是master, 忽略此次更新操作
# 11 : database error
# 21 : 项目目录不存在
# 21 : 项目update failed
@app.task
def auto_deploy(token, push_branch, before, after):
    compile_flag    = None
    project         = mysql_get("SELECT \
                                    P.`id` AS PId, \
                                    P.`alias` AS PAlias, \
                                    P.`webapp_name` AS PWebapp, \
                                    P.`reliable` AS PReliable, \
                                    AR.`host_id` AS ARHId, \
                                    AR.`hg_id` AS ARHGId \
                                FROM \
                                    `t_deploy_auto_rule` AS AR \
                                LEFT JOIN `t_assets_project` AS P ON P.id = AR.proj_id \
                                WHERE \
                                    AR.token = '{}'".format(token))

    # 新建分支
    if before == '0000000000000000000000000000000000000000':
        # 插入 pb project_branch 表
        sql = "INSERT INTO `t_assets_proj_branch` (`branch`, `proj_id`) VALUES ('{}', '{}')".format(
            project['PId'], push_branch
        )
        try:
            pbid = mysql_insert(sql)
        except IntegrityError as e:
            return dict(code=11, column=e.args[1].split()[-1][1:-1])

        # 插入 dh deploy_history 表
        sql = "INSERT INTO `t_deploy_history` (`pb_id`, `event`, `type`, `time`, `after_commit`) " \
              "VALUES ('{}', '{}', '{}', '{}', '{}')".format(
            pbid, 'NEWBRANCH', 'AUTO', time.strftime('%Y-%m-%s %H:%M:%S'), after
        )

        try:
            dhid = mysql_insert(sql)
        except IntegrityError as e:
            return dict(code=11, column=e.args[1].split()[-1][1:-1])

    # 删除分支
    if after == '0000000000000000000000000000000000000000':
        # pb project_branch 表 删除记录
        sql = "DELETE FROM `t_assets_proj_branch` WHERE proj_id='{}' AND branch='{}'".format(
            project['PId'], push_branch
        )
        try:
            mysql_delete(sql)
        except IntegrityError as e:
            return dict(code=11, column=e.args[1].split()[-1][1:-1])

    # 非master分支不自动发布
    if push_branch != 'master':
        return dict(code=1,branch=push_branch)
    else:
        # 获取项目需要发布到的机器及路径(container)
        containers = get_containers(project)

        proj_repo_path = '/var/autop/repo/{}___master'.format(project['PAlias'])

        # 切换目录
        try:
            os.chdir(proj_repo_path)
        except:
            return dict(code=21)

        # update
        try:
            os.system('git pull')
        except:
            return dict(code=31)



# Functions used in tasks above
def get_containers(proj):
    containers = list()
    if proj['PReliable']==0:
        # 根据 proj 结果看 项目是发布到 主机 还是 主机组
        if proj['ARHId']:
            containers.append(
                    mysql_get(
                            "SELECT `ip_addr` FROM `t_assets_host` WHERE id='{}'".format(proj['ARHId'])
                    )['ip_addr'].encode() + ":" + proj['PWebapp']
            )
        elif proj['ARHGId']:
            hosts = mysql_query(
                        "SELECT `ip_addr` FROM `t_assets_host` WHERE hg_id='{}'".format(proj['ARHGId'])
                    )
            for h in hosts:
                containers.append(h['ip_addr'].encode() + ":" + proj['PWebapp'])
    return containers
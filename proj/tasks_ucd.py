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
# 31 : 编译失败
# 41 : 发布失败
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
        # 切换目录
        proj_repo_path = '/var/autop/repo/{}___master'.format(project['PAlias'])
        try:
            os.chdir(proj_repo_path)
        except:
            return dict(code=21)

        # update
        try:
            os.system('git pull')
        except:
            return dict(code=31)

        # 获取项目需要发布到的机器及路径(container)
        containers = get_containers(project)
        # 获取更新的文件
        src_files, compile_flag = get_update_files(before, after)

        if compile_flag:
            try:
                subprocess.check_output('mvn clean install', shell=True)
            except Exception as e:
                return dict(type=type(e).__name__, info=traceback.format_exc(), code=31)

        # 发布文件
        return deploy_incremental(src_files, containers)

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
    elif proj['PReliable']==1:
        sql = "SELECT \
                    P.`id` AS PId, \
                    P.`alias` AS PAlias, \
                    P.`webapp_name` AS PWebapp, \
                    P.`reliable` AS PReliable, \
                    AR.`host_id` AS ARHId, \
                    AR.`hg_id` AS ARHGId \
                FROM \
                    `t_assets_project` AS P \
                LEFT JOIN `t_deploy_auto_rule` AS AR ON AR.proj_id = P.id \
                WHERE \
                    P.rely_id = {}".format(proj['PId'])
        relies = mysql_query(sql)
        for proj in relies:
            containers += get_containers(proj)
    return containers

def get_update_files(before, after):
    compile_flag = None
    src_files = dict()
    diff_result =  filter(lambda x:x,
                        subprocess.check_output('git diff --name-status {old_commit} {new_commit}'.
                            format(
                                old_commit = before, new_commit = after
                            ),
                            shell=True).split('\n')
                        )
    for f in diff_result:
        statu = f.split('\t')[0]
        file = f.split('\t')[1]

        if file.endswith('java'):
            compile_flag = True
            file = 'target/class'+ file[12:-5] + '.class'

        if src_files.has_key(statu):
            src_files[statu].append(file)
        else:
            src_files[statu] = [file]
    return src_files, compile_flag

def get_dst_path(src_file):
    if src_file.endswith('class'):
        return 'WEB-INF/classes/'+ '/'.join(src_file.split('/')[3:])
    else:
        return '/'.join(src_file.split('/')[3:])

def deploy_incremental(src_files, containers):
    deploy_status = list()
    for f in src_files['M']:
        for container in containers:
            cmd = "scp {src_path} root@{host}:/usr/local/tomcat1/webapps/{webapp}/{dst_path}".format(
                    src_path=f,
                    host=container.split(':')[0],
                    webapp=container.split(':')[1],
                    dst_path=get_dst_path(f)
            )
            try:
                os.system(cmd)
            except Exception as e:
                deploy_status.append('D###ERROR###{host}###{file}'.format(host=container.split(':')[0], file=f))
            deploy_status.append('D###OK###{host}###{file}'.format(host=container.split(':')[0], file=f))
    for f in src_files['A']:
        for container in containers:
            cmd = "scp {src_path} root@{host}:/usr/local/tomcat1/webapps/{webapp}/{dst_path}".format(
                    src_path=f,
                    host=container.split(':')[0],
                    webapp=container.split(':')[1],
                    dst_path=get_dst_path(f)
            )
            try:
                os.system(cmd)
            except Exception as e:
                deploy_status.append('D###ERROR###{host}###{file}'.format(host=container.split(':')[0], file=f))
            deploy_status.append('D###OK###{host}###{file}'.format(host=container.split(':')[0], file=f))
    for f in src_files['D']:
        for container in containers:
            cmd = "ssh root@{host} 'rm -rf /usr/local/tomcat1/webapps/{webapp}/{dst_path}'".format(
                    host=container.split(':')[0],
                    webapp=container.split(':')[1],
                    dst_path=get_dst_path(f)
            )
            try:
                os.system(cmd)
            except Exception as e:
                deploy_status.append('D###ERROR###{host}###{file}'.format(host=container.split(':')[0],file=f))
            deploy_status.append('D###OK###{host}###{file}'.format(host=container.split(':')[0], file=f))
    return dict(code=0, result=deploy_status)

def deploy_full(artifact, containers, proj_webapp):
    deploy_status = list()
    for container in containers:
        cmd = "scp {artifact} root@{host}:/usr/local/tomcat1/{artifact_root}/{webapp}".format(
            artifact = artifact,
            host = container.split(':')[0],
            artifact_root=container.split(':')[1],
            webapp=proj_webapp
        )
        try:
            os.system(cmd)
        except Exception as e:
            deploy_status.append('D###ERROR###{host}'.format(host=container.split(':')[0] ))
        deploy_status.append('D###OK###{host}'.format(host=container.split(':')[0]))
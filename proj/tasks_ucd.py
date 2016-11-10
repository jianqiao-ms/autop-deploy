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
    project         = mysql_get("SELECT \
                                    P.`id` AS PId, \
                                    P.`alias` AS PAlias, \
                                    P.`webapp_name` AS PWebapp, \
                                    P.`reliable` AS PReliable, \
                                    P.`full_update` AS PFullUpdate, \
                                    P.`artifact` AS PArtifact, \
                                    AR.`host_id` AS ARHId, \
                                    AR.`hg_id` AS ARHGId \
                                FROM \
                                    `t_deploy_auto_rule` AS AR \
                                LEFT JOIN `t_assets_project` AS P ON P.id = AR.proj_id \
                                WHERE \
                                    AR.token = '{}'".format(token))

    print(project)

    # 判断是否 新建或删除分支
    bool, evt = is_branch_level(before,after)
    if bool:
        sql_pb_a = "INSERT INTO `t_assets_proj_branch` (`branch`, `proj_id`) \
                      VALUES ('{id}', '{branch}')".format(
                        id=project['PId'], branch=push_branch
                    )
        sql_pb_d = "UPDATE `t_assets_proj_branch` SET `status`='DELETED' \
                      WHERE `proj_id`='{id}' AND `branch`='{branch}'".format(
                        id=project['PId'], branch=push_branch
                    )
        try:
            pbid = mysql_insert(sql_pb_a) if evt=='add' else mysql_update(sql_pb_d)
            sql_dh = "INSERT INTO `t_deploy_history` (`pb_id`, `event`, `type`, `time`, `before_commit`, `after_commit`) \
                        VALUES ('{}', '{}', '{}', '{}', '{}', '{}')".format(
                          pbid,
                          'ADDBRANCH' if evt == 'add' else 'DELBRANCH',
                          'AUTO',
                          time.strftime('%Y-%m-%d %H:%M:%S'),
                          before,
                          after
                      )
            mysql_insert(sql_dh)
        except Exception as e:
            print(dict(code=11, info=traceback.format_exc()))
            return traceback.format_exc().split('\n')

    # 非master分支不自动发布
    if push_branch != 'master':
        print(dict(code=1,branch=push_branch))
    else:
        # 切换目录
        proj_repo_path = '/var/autop/repo/{}___master'.format(project['PAlias'])
        try:
            os.chdir(proj_repo_path)
        except:
            print(dict(code=21))

        # update
        try:
            subprocess.check_call('git pull', shell=True)
            print('[LOG]update success')
        except:
            print(dict(code=31))
            return traceback.format_exc().split('\n')

        # 获取更新的文件 编译
        src_files, compile_flag = get_update_files(before, after, project['PFullUpdate'], project['PArtifact'])
        if compile_flag:
            try:
                subprocess.check_call('mvn clean install', shell=True)
                print('[LOG]compile success')
            except Exception as e:
                print(dict(type=type(e).__name__, info=traceback.format_exc(), code=31))
                return traceback.format_exc().split('\n')
        else:
            print('[LOG]compile skip')

        # 获取项目需要发布到的机器及路径(container)
        containers = get_containers(project)
        for c in containers:
            print(c)
        print('[LOG]get containers success')
        # 发布文件
        sql = "SELECT `id` FROM `t_assets_proj_branch` WHERE `proj_id`='{}' AND `branch`='master'".format(
                project['PId']
        )
        pbid = mysql_get(sql)['id']
        try:
            deploy_status = deploy(src_files, containers)
            sql = "INSERT INTO `t_deploy_history` (`pb_id`,`type`, `event`, `time`, `before_commit`, `after_commit`) \
                                  VALUES ('{}', '{}', '{}', '{}', '{}', '{}')".format(
                    pbid, 'AUTO', 'PUSH', time.strftime('%Y-%m-%d %H:%M:%S'), before, after
            )
            mysql_insert(sql)
            for l in deploy_status:
                print(l)
            return deploy_status
        except Exception as e:
            print(e)
            return traceback.format_exc().split('\n')

# Functions used in tasks above
def is_branch_level(before, after):
    if before == '0000000000000000000000000000000000000000' \
            or after == '0000000000000000000000000000000000000000':
        return True, 'add' if before == '0000000000000000000000000000000000000000' else 'del'
    else:
        return False, None

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

def get_update_files(before, after, full_update, artifact):
    compile_flag = None
    src_files = None
    if not full_update:
        src_files = dict()
        diff_result =  filter(lambda x:x,
                                subprocess.check_output(
                                        'git diff --name-status {old_commit} {new_commit}'.format(
                                            old_commit = before, new_commit = after
                                            ),shell=True
                                ).split('\n')
                            )
        for f in diff_result:
            statu = f.split('\t')[0]
            file = f.split('\t')[1]

            if file.endswith('java'):
                compile_flag = True
                file = 'target/classes'+ file[13:-5] + '.class'

            if src_files.has_key (statu):
                src_files[statu].append(file)
            else:
                src_files[statu] = [file]
    else:
        src_files = 'target/'+artifact
        compile_flag = True
    return src_files, compile_flag

def get_dst_path(src_file):
    if src_file.endswith('class'):
        return 'WEB-INF/classes/'+ '/'.join(src_file.split('/')[2:])
    else:
        return '/'.join(src_file.split('/')[3:])

def deploy(src_files, containers):
    deploy_status = list()
    if isinstance(src_files, dict):
        for f in src_files['M'] if src_files.has_key('M') else []:
            for container in containers:
                cmd = "scp {src_path} root@{host}:/usr/local/tomcat1/webapps/{webapp}/{dst_path}".format(
                        src_path=f,
                        host=container.split(':')[0],
                        webapp=container.split(':')[1],
                        dst_path=get_dst_path(f)
                )
                print(cmd)
                try:
                    subprocess.check_call(cmd, shell=True)
                except Exception as e:
                    print(e.message)
                    deploy_status.append('D###ERROR###{host}###{file}###{error}'.format(host=container.split(':')[0], file=f, error=e.message))
                    continue
                deploy_status.append('D###OK###{host}###{file}'.format(host=container.split(':')[0], file=f))
        for f in src_files['A'] if src_files.has_key('A') else []:
            for container in containers:
                cmd = "scp {src_path} root@{host}:/usr/local/tomcat1/webapps/{webapp}/{dst_path}".format(
                        src_path=f,
                        host=container.split(':')[0],
                        webapp=container.split(':')[1],
                        dst_path=get_dst_path(f)
                )
                print(cmd)
                try:
                    subprocess.check_call(cmd, shell=True)
                except Exception as e:
                    print(e.message)
                    deploy_status.append(
                        'D###ERROR###{host}###{file}###{error}'.format(host=container.split(':')[0], file=f, error=e.message))
                    continue
                deploy_status.append('D###OK###{host}###{file}'.format(host=container.split(':')[0], file=f))
        for f in src_files['D'] if src_files.has_key('D') else []:
            for container in containers:
                cmd = "ssh root@{host} 'rm -rf /usr/local/tomcat1/webapps/{webapp}/{dst_path}'".format(
                        host=container.split(':')[0],
                        webapp=container.split(':')[1],
                        dst_path=get_dst_path(f)
                )
                print(cmd)
                try:
                    subprocess.check_call(cmd, shell=True)
                except Exception as e:
                    print(e.message)
                    deploy_status.append(
                        'D###ERROR###{host}###{file}###{error}'.format(host=container.split(':')[0], file=f, error=e.message))
                    continue
                deploy_status.append('D###OK###{host}###{file}'.format(host=container.split(':')[0], file=f))
    elif isinstance(src_files, unicode):
        for container in containers:
            cmd = "scp {src_path} root@{host}:/usr/local/tomcat1/webapps/{webapp}/{dst_path}".format(
                    src_path=src_files.encode(),
                    host=container.split(':')[0],
                    webapp=container.split(':')[1],
                    dst_path='WEB-INF/lib'
            )
            print(cmd)
            try:
                subprocess.check_call(cmd, shell=True)
            except Exception as e:
                print(e.message)
                deploy_status.append(
                    'D###ERROR###{host}###{file}###{error}'.format(host=container.split(':')[0], file=src_files, error=e.message))
                continue
            deploy_status.append('D###OK###{host}###{file}'.format(host=container.split(':')[0], file=src_files))
    return deploy_status
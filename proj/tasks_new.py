#!/usr/bin/env python2
# -*- coding:UTF-8 -*-

# celery app 子模块必须引入的包
from __future__ import absolute_import

from pyasn1.type.univ import Null

from proj.celery import app
from proj.db import mysql_insert
from proj.db import mysql_delete
from proj.db import mysql_update
from proj.db import mysql_query
from proj.db import mysql_get

# 异常
from torndb import IntegrityError
from socket import gaierror

# 功能性import
import os
import time
import subprocess
import paramiko
import traceback
import random
import string

@app.task
def new_host(envId, ipaddr, hgId, uName, uPwd):
    response = os.system('ping -c 1 {}'.format(ipaddr))
    response >>= 8
    if response == 1:
        return dict(code=100)
    if response == 2:
        return dict(code=101)

    ssh = paramiko.SSHClient()                                  # 初始化SSHClient对象
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    hostname=None                                               # 初始化hostname
    try:
        if len(uPwd):
            print('password')
            ssh.connect(ipaddr, port=22, username='root', password=uPwd, timeout=5)
        else:
            print('none password')
            ssh.connect(ipaddr, port=22, username='root', timeout=5)
        stdin, stdout, stderr = ssh.exec_command("hostname")
        hostname = stdout.readlines()[0]
    except gaierror:
        return dict(code=200)
    except paramiko.AuthenticationException:
        return dict(code=300)
    except paramiko.ssh_exception.NoValidConnectionsError:
        return dict(code=310)
    except paramiko.SSHException:
        return dict(code=301)
    except Exception as e:
        return dict(type=type(e).__name__, info=traceback.format_exc(), code=400)
    finally:
        ssh.close()

    try:
        sql = "INSERT INTO `t_assets_host` (`hostname`, `ip_addr`, `env_id`, `group_id`) " \
              "VALUES ('{}', '{}', '{}', '{}')".format(hostname, ipaddr, envId, hgId)
        mysql_insert(sql)
        return dict(code=0)
    except IntegrityError:
        return dict(code=11)
    except Exception as e:
        return dict(type=type(e).__name__, info=traceback.format_exc(), code=400)


@app.task
def new_hostgroup(envId, hgName, hgDes):
    try:
        sql = "INSERT INTO `t_assets_hostgroup` (`env_id`, `name`, `description`) " \
              "VALUES ('{}', '{}', '{}')".format(envId, hgName, hgDes)
        mysql_insert(sql)
        return dict(code=0)
    except IntegrityError:
        return dict(code=11)
    except Exception as e:
        return dict(type=type(e).__name__, info=traceback.format_exc(), code=400)

# Description of return code
#
# 1 : project directory exist
# 11 : database error
# 100 : error reading repo infomation
@app.task
def new_project(repo, alias, webapp, reliable, rely_id):
    try:
        result = subprocess.check_output(
                'export GIT_TERMINAL_PROMPT=0;git ls-remote --heads {}'.
                    format(repo), shell=True).split('\n')
    except Exception as e:
        return dict(type=type(e).__name__, info=traceback.format_exc(), code=400)

    name, alias, webapp = get_proj_name(repo, alias, webapp)
    pid = None  #新项目id
    pbid = None #项目、分支id
    dhid = None #发布历史id
    try:
        sql = "INSERT INTO `t_assets_project` (`repo`, `name`, `alias`, `webapp_name`, `reliable`, `rely_id`) \
              VALUES ('{}', '{}', '{}', '{}', '{}','{}')".format(repo, name, alias, webapp, reliable,rely_id if rely_id else 0)
        pid = mysql_insert(sql)

        p_path = prepare_proj_dir(name, alias, 'master')
        subprocess.check_call('git clone {} {}'.format(repo, p_path), shell=True)

        for r in result:
            if not r.lstrip().rstrip():
                continue
            branch = r.split('\t')[1].split('/')[2]
            if branch=='master':
                continue
            pb_path = prepare_proj_dir(name, alias, branch)
            os.system('cp -r {} {}'.format(p_path, pb_path))
            os.chdir(pb_path)
            os.system('git checkout -b {} -t origin/{}'.format(branch, branch))

            sql = "INSERT INTO `t_assets_proj_branch` (`proj_id`, `branch`) " \
                  "VALUES ('{}', '{}')".format(pid, branch)
            pbid = mysql_insert(sql)

            sql = "INSERT INTO `t_deploy_history` (`pb_id`, `event`, `type`, `time`, `after_commit`) " \
                  "VALUES ('{}', 'INIT', 'manual', '{}', '{}')".format(pbid, time.strftime('%Y-%m-%d %H:%M:%S'),r.split('t')[0])
            dhid = mysql_insert(sql)

        return dict(code=0)
    except IntegrityError as e:
        return dict(code=11, column=e.args[1].split()[-1][1:-1])
    except Exception as e:
        if pid:
            mysql_delete('DELETE FROM `t_assets_project` WHERE `id`={}'.format(pid))
        if pbid:
            mysql_delete('DELETE FROM `t_assets_proj_branch` WHERE `id`={}'.format(pbid))
        if dhid:
            mysql_delete('DELETE FROM `t_deploy_history` WHERE `id`={}'.format(dhid))
        return dict(type=type(e).__name__, info=traceback.format_exc(), code=400)

@app.task
def new_autorule(pid, container):
    try:
        sql=None
        token = ''.join(random.sample(string.ascii_letters+string.digits, 13))
        if container.startswith('g'):
            sql = "INSERT INTO `t_deploy_auto_rule` (`proj_id`, `proj_branch`, `hg_id`, `token`) " \
                  "VALUES ('{}', '{}', '{}', '{}')".format(pid, 'master', container[1:], token)
        elif container.startswith('h'):
            sql = "INSERT INTO `t_deploy_auto_rule` (`proj_id`, `proj_branch`, `host_id`, `token`) " \
                  "VALUES ('{}', '{}', '{}', '{}')".format(pid, 'master', container[1:], token)
        else:
            sql = "INSERT INTO `t_deploy_auto_rule` (`proj_id`, `proj_branch`, `token`) " \
                  "VALUES ('{}', '{}', '{}')".format(pid, 'master', token)
        mysql_insert(sql)
        return dict(code=0)
    except IntegrityError as e:
        return dict(code=11, column=e.args[1].split()[-1][1:-1])
    except Exception as e:
        return dict(type=type(e).__name__, info=traceback.format_exc(), code=400)




# Functions used in tasks above
def get_proj_name(_repo, _alias, _webapp):
    _name = _repo.split('.git')[0].split('/')[-1]
    if not _alias:
        _alias = _name
    if not _webapp:
        _webapp = _name
    return _name, _alias, _webapp
def prepare_proj_dir(_name, _alias, branch):
    if len(_alias) == 0:
        _alias = _name
    _p_path = '/var/autop/repo/{}___{}'.format(_alias, branch)
    if os.path.exists(_p_path):
        os.system('rm -rf {}'.format(_p_path))
    return _p_path
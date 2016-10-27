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
import os
import paramiko
import traceback
import random
import string

@App.task
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
        db_conn.insert(sql)
        return dict(code=0)
    except IntegrityError:
        return dict(code=11)
    except Exception as e:
        return dict(type=type(e).__name__, info=traceback.format_exc(), code=400)


@App.task
def new_hostgroup(envId, hgName, hgDes):
    try:
        sql = "INSERT INTO `t_assets_hostgroup` (`env_id`, `name`, `description`) " \
              "VALUES ('{}', '{}', '{}')".format(envId, hgName, hgDes)
        db_conn.insert(sql)
        return dict(code=0)
    except IntegrityError:
        return dict(code=11)
    except Exception as e:
        return dict(type=type(e).__name__, info=traceback.format_exc(), code=400)

@App.task
def new_project(repo, alias, rely):
    try:
        response = os.system('export GIT_TERMINAL_PROMPT=0;git ls-remote {}'.format(repo))
        if response!=0:
            return dict(code=100)
    except Exception as e:
        return dict(type=type(e).__name__, info=traceback.format_exc(), code=400)
    try:
        name = repo.split('.git')[0].split('/')[-1]
        if len(alias)==0:
            alias=name
        pPath = '/var/autop/repo/{}___master'.format(alias)
        if os.path.exists(pPath):
            return dict(code=1)
        else:
            os.system('git clone {} {}'.format(repo,pPath))

        sql = "INSERT INTO `t_assets_project` (`repo`, `name`, `alias`, rely) " \
              "VALUES ('{}', '{}', '{}', '{}')".format(repo, name, alias, rely)
        db_conn.insert(sql)
        return dict(code=0)
    except IntegrityError as e:
        return dict(code=11, column=e.args[1].split()[-1][1:-1])
    except Exception as e:
        return dict(type=type(e).__name__, info=traceback.format_exc(), code=400)

@App.task
def new_autorule(pid, container):
    try:
        sql=None
        if container.startswith('g'):
            sql = "INSERT INTO `t_deploy_auto_rule` (`project_id`, `project_branch`, `hg_id`, `token`) " \
                  "VALUES ('{}', '{}', '{}', '{}')".format(pid, 'master', container[1:], ''.join(random.sample(string.ascii_letters+string.digits, 13)))
        else:
            sql = "INSERT INTO `t_deploy_auto_rule` (`project_id`, `project_branch`, `host_id`, `token`) " \
                  "VALUES ('{}', '{}', '{}', '{}')".format(pid, 'master', container[1:], ''.join(random.sample(string.ascii_letters+string.digits, 13)))
        db_conn.insert(sql)
        return dict(code=0)
    except IntegrityError as e:
        return dict(code=11, column=e.args[1].split()[-1][1:-1])
    except Exception as e:
        return dict(type=type(e).__name__, info=traceback.format_exc(), code=400)
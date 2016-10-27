#!/usr/bin/env python2
# -*- coding:UTF-8 -*-

from __future__ import absolute_import
from worker.app import App
from worker.db import db_conn
from torndb import IntegrityError

import os
import paramiko
import traceback
from socket import gaierror

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
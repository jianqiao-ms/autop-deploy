#!/usr/bin/env python2.7
# -*- coding:UTF-8 -*-

import torndb
from celery import Celery

import os
import re
import sys
import time
import traceback
import subprocess
import ipaddress
import paramiko
import socket
import random
import string

celery = Celery("task")
celery.config_from_object('celeryconf')

class Connection(torndb.Connection):
    def execute_rowcount(self, query, *parameters, **kwparameters):
        super(Connection, self).execute_rowcount(query, *parameters, **kwparameters)

    update = delete = execute_rowcount

db = Connection(host="192.168.0.195",database="autop",user='cupid',password='everyone2xhfz')

p_git_updated_file = re.compile(r'^(?!D)\t*.+$')
p_git_deleted_file = re.compile(r'^(?=D)\t*.+$')

@celery.task
def mysql_query(cmd):
    return db.query(cmd)
@celery.task
def mysql_get(cmd):
    return db.query(cmd)
@celery.task
def deploy(pname):
    name_path = {'imanager_web'     : 'imanager_web',
                 'api'              : 'imanager_api',
                 'imanager_core'    :  'imanager',
                 'iclock'           : 'imanager_iclock',
                 'iservice'         : 'imanager_iservice',
                 'actor'            : 'iservice',
                 'oa'               : 'oa',
                 }

    name_host = {'imanager_web'     : ['192.168.0.105', 'imanager'],
                 'api'              : ['192.168.0.126', 'api'],
                 'imanager_core'    : ['ALL'],
                 'iclock'           : ['192.168.0.81','iclock'],
                 'iservice'         : ['192.168.0.112','192.168.0.111','iservice'],
                 'actor'            : ['192.168.0.150', '192.168.0.151', '192.168.0.152', 'iservice'],
                 'oa'               : ['192.168.0.91', 'oa'],
                 }

    data = dict()
    data['msg']  = list()
    data['code'] = 200
    flag = None

    # 切换目录
    data['msg'].append('[OK]检测项目repo')
    path = "/var/autop/repo/{path}".format(path = name_path[pname])
    if os.path.isdir(path):
        os.chdir(path)
        data['msg'].append('[OK]项目repo 存在')
        data['msg'].append('[OK]切换到项目repo {path}'.format(path = path))
    else:
        data['msg'].append('[WARNNING]项目repo 不存在，初始化项目')
        os.chdir('/var/autop/repo')
        try:
            subprocess.check_output('git clone http://192.168.1.141/devs/{pname}.git'.format(pname = name_path[pname]), shell=True)
            data['msg'].append('[OK]项目初始化成功')
            os.chdir(path)
        except subprocess.CalledProcessError,e:
            data['msg'].append('[ERROR]clone项目失败')
            for line in e.output.split('\n'):
                data['msg'].append('\t{line}'.format(line = line))
            data['code'] = sys._getframe().f_lineno
            return data
        except:
            data['msg'].append('[ERROR]clone项目失败')
            for line in traceback.format_exc().split('\n'):
                data['msg'].append('\t{line}'.format(line = line))
            data['code'] = sys._getframe().f_lineno
            return data

    # 更新项目
    try:
        updated_file = []
        deleted_file = []
        result = subprocess.check_output("git pull", shell=True).split('\n')
        data['msg'].append('[OK]git更新成功')
        if result[0] == 'Already up-to-date.':
            data['msg'].append('[WARN]已经是最新,发布取消')
            return data
        else:
            commit_start = result[0].split()[1].split('..')[0]
            commit_stop = result[0].split()[1].split('..')[1]

            changes = subprocess.check_output("git diff --name-status {start} {stop}".
                                              format(start = commit_start, stop = commit_stop),
                                              shell= True).split('\n')
            deleted_file    = map(lambda x:x.split()[1], filter(lambda x:p_git_deleted_file.match(x), changes))
            updated_file    = map(lambda x:x.split()[1], filter(lambda x:p_git_updated_file.match(x), changes))
    except subprocess.CalledProcessError, e:
        data['msg'].append('[ERROR]git更新失败')
        for line in e.output.split('\n'):
            data['msg'].append('\t{line}'.format(line = line))
        data['code'] = sys._getframe().f_lineno
        return data
    except:
        data['msg'].append('[ERROR]git更新失败')
        for line in traceback.format_exc().split('\n'):
            data['msg'].append('\t{line}'.format(line = line))
        data['code'] = sys._getframe().f_lineno
        return data

    # 编译项目
    compile_flag = False
    for f in updated_file:
        if f.endswith('.java'):
            compile_flag = True
            break

    if compile_flag:
        try:
            subprocess.check_output("mvn clean install", shell = True)
            data['msg'].append('[OK]编译成功')
        except subprocess.CalledProcessError, e:
            data['msg'].append('[ERROR]编译失败')
            for line in traceback.format_exc().split('\n'):
                data['msg'].append('\t{line}'.format(line=line))
            for line in e.output.split('\n'):
                data['msg'].append('\t{line}'.format(line = line))
            data['code'] = sys._getframe().f_lineno
            return data
        except:
            data['msg'].append('[ERROR]编译失败')
            for line in traceback.format_exc().split('\n'):
                data['msg'].append('\t{line}'.format(line = line))
            data['code'] = sys._getframe().f_lineno
            return data
    else:
        data['msg'].append('[WARN]没有java文件更新,跳过编译')

    # # 发布项目
    if pname != 'imanager_core':
        for f in updated_file:
            if f=='.gitlab-ci.yml':
                continue
            cmd = None
            if f.endswith('.java') and f.startswith('src/main/java'):
                f = 'target/class' + f.split('src/main/java')[1][:-4] + 'class'
                cmd = 'pscp -H "{hosts}" -l root {file} /usr/local/tomcat1/webapps/{webapp}/{path}'.\
                    format(hosts    = ' '.join(name_host[pname][:-1]),
                           file     = f,
                           webapp   = name_host[pname][-1],
                           path     = 'WEB-INF/class'+f.split('target/class')[1])
            elif f.startswith('src/main/java') and not f.endswith('.java'):
                cmd = 'pscp -H "{hosts}" -l root {file} /usr/local/tomcat1/webapps/{webapp}/{path}'. \
                    format(hosts    = ' '.join(name_host[pname][:-1]),
                           file     = f,
                           webapp   = name_host[pname][-1],
                           path     = 'WEB-INF/class' + f.split('src/main/java')[1])
            elif f.startswith('src/main/resource'):
                cmd = 'pscp -H "{hosts}" -l root {file} /usr/local/tomcat1/webapps/{webapp}/{path}'. \
                    format(hosts    = ' '.join(name_host[pname][:-1]),
                           file     = f,
                           webapp   = name_host[pname][-1],
                           path     = 'WEB-INF/class' + f.split('src/main/resource')[1])
            elif f.startswith('src/main/webapp'):
                cmd = 'pscp -H "{hosts}" -l root {file} /usr/local/tomcat1/webapps/{webapp}/{path}'. \
                    format(hosts    = ' '.join(name_host[pname][:-1]),
                           file     = f,
                           webapp   = name_host[pname][-1],
                           path     = f.split('src/main/webapp')[1])

            try:
                subprocess.check_output(cmd, shell=True)
                data['msg'].append('[OK]发布成功\t{file}'.format(file = f))
            except subprocess.CalledProcessError, e:
                data['msg'].append('[ERROR]{file}发布失败'.format(file = f))
                for line in e.output.split('\n'):
                    data['msg'].append('\t{line}'.format(line=line))
                data['code'] = sys._getframe().f_lineno
                pass
            except:
                data['msg'].append('[ERROR]{file}发布失败'.format(file = f))
                for line in traceback.format_exc().split('\n'):
                    data['msg'].append('\t{line}'.format(line = line))
                data['code'] = sys._getframe().f_lineno
                pass
        return data
    else:
        for p in name_host:
            if p == 'imanager_core':
                continue
            if p == 'oa':
                continue
            cmd = 'pscp -H "{hosts}" -l root target/imanager_core-0.0.1-SNAPSHOT.jar ' \
                  '/usr/local/tomcat1/webapps/{webapp}/WEB-INF/lib'.\
                format(hosts  = ' '.join(name_host[p][:-1]),
                       webapp = name_host[p][-1])

            try:
                subprocess.check_output(cmd, shell=True)
                data['msg'].append('[OK]imanager_core发布到{project:20}@ {host}成功'.format(project = p, host = ' '.join(name_host[p][:-1])))
            except subprocess.CalledProcessError, e:
                data['msg'].append('[ERROR]imanager_core发布到{project:20}失败'.format(project = p))
                for line in e.output.split('\n'):
                    data['msg'].append('\t{line}'.format(line = line))
                data['code'] = sys._getframe().f_lineno
                pass
            except:
                data['msg'].append('[ERROR]imanager_core发布到{project:20}失败'.format(project=p))
                for line in traceback.format_exc().split('\n'):
                    data['msg'].append('\t{line}'.format(line = line))
                data['code'] = sys._getframe().f_lineno
                pass
        return data

@celery.task
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
            print 'password'
            ssh.connect(ipaddr, port=22, username='root', password=uPwd, timeout=5)
        else:
            print 'none password'
            ssh.connect(ipaddr, port=22, username='root', timeout=5)
        stdin, stdout, stderr = ssh.exec_command("hostname")
        hostname = stdout.readlines()[0]
    except socket.gaierror:
        return dict(code=200)
    except paramiko.AuthenticationException:
        return dict(code=300)
    except paramiko.ssh_exception.NoValidConnectionsError:
        return dict(code=310)
    except paramiko.SSHException:
        return dict(code=301)
    except Exception,e:
        return dict(type=type(e).__name__, info=traceback.format_exc(), code=400)
    finally:
        ssh.close()

    try:
        sql = "INSERT INTO `t_assets_host` (`hostname`, `ip_addr`, `env_id`, `group_id`) " \
              "VALUES ('{}', '{}', '{}', '{}')".format(hostname, ipaddr, envId, hgId)
        print sql
        db.insert(sql)
        return dict(code=0)
    except torndb.IntegrityError:
        return dict(code=11)
    except Exception, e:
        return dict(type=type(e).__name__, info=traceback.format_exc(), code=400)

@celery.task
def new_hostgroup(envId, hgName, hgDes):
    try:
        sql = "INSERT INTO `t_assets_hostgroup` (`env_id`, `name`, `description`) " \
              "VALUES ('{}', '{}', '{}')".format(envId, hgName, hgDes)
        db.insert(sql)
        return dict(code=0)
    except torndb.IntegrityError:
        return dict(code=11)
    except Exception, e:
        return dict(type=type(e).__name__, info=traceback.format_exc(), code=400)

@celery.task
def new_project(repo, alias):
    try:
        response = os.system('export GIT_TERMINAL_PROMPT=0;git ls-remote {}'.format(repo))
        if response!=0:
            return dict(code=100)
    except Exception, e:
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

        sql = "INSERT INTO `t_assets_project` (`repo`, `name`, `alias`) " \
              "VALUES ('{}', '{}', '{}')".format(repo, name, alias)
        db.insert(sql)
        return dict(code=0)
    except torndb.IntegrityError,e:
        return dict(code=11, column=e.args[1].split()[-1][1:-1])
    except Exception, e:
        return dict(type=type(e).__name__, info=traceback.format_exc(), code=400)

@celery.task
def new_autorule(pid, container):
    try:
        sql=None
        if container.startswith('g'):
            sql = "INSERT INTO `t_deploy_auto_rule` (`project_id`, `project_branch`, `hg_id`, `token`) " \
                  "VALUES ('{}', '{}', '{}', '{}')".format(pid, 'master', container[1:], ''.join(random.sample(string.ascii_letters+string.digits, 13)))
        else:
            sql = "INSERT INTO `t_deploy_auto_rule` (`project_id`, `project_branch`, `host_id`, `token`) " \
                  "VALUES ('{}', '{}', '{}', '{}')".format(pid, 'master', container[1:], ''.join(random.sample(string.ascii_letters+string.digits, 13)))
        db.insert(sql)
        return dict(code=0)
    except torndb.IntegrityError, e:
        return dict(code=11, column=e.args[1].split()[-1][1:-1])
    except Exception, e:
        return dict(type=type(e).__name__, info=traceback.format_exc(), code=400)


@celery.task
def del_autorule(arid):
    try:
        sql = 'SELECT alias FROM `t_assets_project` p LEFT JOIN `t_deploy_auto_rule` ar ON ar.project_id=p.id WHERE ar.id={}'.format(arid)
        pAlias = db.get(sql)['alias']
        pPath = '/var/autop/repo/{}___master'.format(pAlias)
        if os.path.exists(pPath):
            os.system('rm -rf {}'.format(pPath))
        sql = "DELETE FROM `t_deploy_auto_rule` WHERE id={}".format(arid)
        db.delete(sql)
        return dict(code=0)
    except torndb.IntegrityError, e:
        return dict(code=11, column=e.args[1].split()[-1][1:-1])
    except Exception, e:
        return dict(type=type(e).__name__, info=traceback.format_exc(), code=400)
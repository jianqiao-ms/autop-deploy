#!/usr/bin/env python2
# -*- coding:UTF-8 -*-

# 系统包
from __future__ import absolute_import
from tornado.gen import coroutine

# 三方包
import torncelery

# 自定义包
from server import BaseHandler

from proj.db import mysql_insert
from proj.db import mysql_delete
from proj.db import mysql_update
from proj.db import mysql_query
from proj.db import mysql_get

from proj.tasks_new import new_host
from proj.tasks_new import new_hostgroup
from proj.tasks_new import new_project
from proj.tasks_new import new_autorule

from proj.tasks_del import del_autorule

class Admin(BaseHandler, object):
    @coroutine
    def get(self, module=''):
        main_content_sql = dict(host        = "SELECT "
                                                "H.`id`                          AS HId,"
                                                "H.`ip_addr`                     AS HIp,"
                                                "H.`hostname`                    AS HName,"
                                                "IFNULL(ENV.`name`,'')           AS EName,"
                                                "IFNULL(HG.`id`,'')              AS HGroupId,"
                                                "IFNULL(HG.`name`,'')            AS HGName "
                                              "FROM `t_assets_host`              AS H "
                                              "LEFT JOIN `t_assets_hostgroup`    AS HG "
                                              "ON H.`group_id` = HG.`id` "
                                              "LEFT JOIN `t_assets_env`          AS ENV "
                                              "ON ENV.`id`=H.`env_id`",
                                hostgroup    = 'SELECT '
                                                 'HG.id                          AS HGId,'
                                                 'HG.`name`                      AS HGName,'
                                                 'HG.description                 AS HGDes,'
                                                 'ENV.`name`                     AS EName '
                                               'FROM `t_assets_hostgroup`        AS HG '
                                               'LEFT JOIN t_assets_env           AS ENV '
                                               'ON ENV.id=HG.env_id',
                                project      = 'SELECT '
                                                 'id                             AS PId,'
                                                 'repo                           AS PRepo,'
                                                 'alias                          AS PAlias, '
                                                 'deploy_alone                   AS PDeployAlone, '
                                                 'IFNULL(`rely_id`,"")           AS PRely, '
                                                 'IFNULL(`webapp_name`,"")       AS PWebapp, '
                                                 'able_to_be_rely                AS PIsRely '
                                               'FROM `t_assets_project`')

        if len(module):
            data = dict()

            main_content = yield torncelery.async(mysql_get, main_content_sql[module])
            data['main_content'] = main_content

            if module=='host':
                data['env'] = yield torncelery.async(mysql_get, 'SELECT * FROM `t_assets_env`')
                data['hostgroup'] = yield torncelery.async(mysql_get, 'SELECT * FROM `t_assets_hostgroup`')

            if module == 'hostgroup':
                data['env'] = yield torncelery.async(mysql_get, 'SELECT * FROM `t_assets_env`')

            self.render("admin-{}.html".format(module),data = data)
            return
        self.render('admin.html')


class NewHost(BaseHandler, object):
    @coroutine
    def post(self, *args, **kwargs):
        envId   = self.get_argument('env',      strip=False)
        ipaddr  = self.get_argument('ipaddr',   strip=False)
        hgId    = self.get_argument('hostgroup',strip=False)
        uName   = self.get_argument('username', strip=False)
        uPwd    = self.get_argument('password', strip=False)

        rData = yield torncelery.async(new_host, envId, ipaddr, hgId, uName, uPwd)
        self.write(rData)
class NewHostgroup(BaseHandler, object):
    @coroutine
    def post(self, *args, **kwargs):
        envId   = self.get_argument('env',      strip=False)
        hgName  = self.get_argument('hg-name',  strip=False)
        hgDes   = self.get_argument('hg-des',   strip=False)

        rData = yield torncelery.async(new_hostgroup, envId, hgName, hgDes)
        self.write(rData)
class NewProject(BaseHandler, object):
    @coroutine
    def post(self, *args, **kwargs):
        repo   = self.get_argument('repo',      strip=False)
        pAlias = self.get_argument('alias',     strip=False)
        rely   = self.get_argument('rely',      strip=False)

        rData = yield torncelery.async(new_project, repo, pAlias, rely)
        self.write(rData)

class NewAutoRule(BaseHandler, object):
    @coroutine
    def post(self, *args, **kwargs):
        pId         = self.get_argument('project',      strip=False)
        container   = self.get_argument('Container',    strip=False)

        rData = yield torncelery.async(new_autorule, pId, container)
        self.write(rData)

class DelAutoRule(BaseHandler, object):
    @coroutine
    def post(self, *args, **kwargs):
        arId = self.get_argument('arid')

        rData = yield torncelery.async(del_autorule, arId)
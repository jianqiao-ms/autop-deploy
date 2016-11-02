#!/usr/bin/env python2
# -*- coding:UTF-8 -*-

# 系统包
from __future__ import absolute_import
from tornado.gen import coroutine

# 三方包
import torncelery

# 自定义包
from ._handler import BaseHandler

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
        function_map = dict(
            host = self.get_host,
            hostgroup = self.get_hg,
            project = self.get_proj
        )

        if not len(module):
            self.get_dashboard()
        else:
            yield function_map[module]()

    def get_dashboard(self):
        self.render('admin.html')

    @coroutine
    def get_host(self):
        data = dict()

        sql_host = "SELECT \
                    H.`id` AS HId, \
                    H.`ip_addr` AS HIp, \
                    H.`name` AS HName, \
                    IFNULL(HG.`id`, '') AS HGroupId, \
                    IFNULL(HG.`name`, '') AS HGName \
                FROM \
                    `t_assets_host` AS H \
                LEFT JOIN `t_assets_hostgroup` AS HG ON H.`hg_id` = HG.`id`"
        sql_hg  = "SELECT \
                    HG.`id` AS HGId, \
                    HG.`name` AS HGName, \
                    HG.`description` AS HGDes \
                FROM \
                    `t_assets_hostgroup` AS HG"

        data['host']    = yield torncelery.async(mysql_query, sql_host)
        data['hg']      = yield torncelery.async(mysql_query, sql_hg)
        self.render('admin_host.html', data=data)

    @coroutine
    def get_hg(self):
        data = dict()

        sql_hg = "SELECT \
                    HG.id AS HGId, \
                    HG.`name` AS HGName, \
                    HG.description AS HGDes \
                FROM \
                    `t_assets_hostgroup` AS HG"

        data['hg'] = yield torncelery.async(mysql_query, sql_hg)
        self.render('admin_hostgroup.html', data=data)

    @coroutine
    def get_proj(self):
        data = dict()

        sql_proj = "SELECT \
                        P.`id` AS PId, \
                        P.`repo` AS PRepo, \
                        P.`alias` AS PAlias, \
                        P.`reliable` AS PReliable, \
                        IFNULL(P.`webapp_name`, '') AS PWebapp, \
                        IFNULL(P.`rely_id`, '') AS PRely \
                    FROM \
                        `t_assets_project` AS P"

        data['proj'] = yield torncelery.async(mysql_query, sql_proj)
        self.render('admin_project.html', data=data)

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
#!/usr/bin/env python
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
                        IFNULL(PP.`alias`, '') AS PRely \
                    FROM \
                        `t_assets_project` AS P \
                    LEFT JOIN `t_assets_project` AS PP ON P.`rely_id`=PP.`id`"

        data['proj'] = yield torncelery.async(mysql_query, sql_proj)
        self.render('admin_project.html', data=data)

class NewHost(BaseHandler, object):
    @coroutine
    def post(self, *args, **kwargs):
        ipaddr  = self.get_argument('ipaddr',   strip=False)
        hgId    = self.get_argument('hostgroup',strip=False)
        uName   = self.get_argument('username', strip=False)
        uPwd    = self.get_argument('password', strip=False)

        rData = yield torncelery.async(new_host, ipaddr, hgId, uName, uPwd)
        self.write(rData)
class NewHostgroup(BaseHandler, object):
    @coroutine
    def post(self, *args, **kwargs):
        hgName  = self.get_argument('hg-name',  strip=False)
        hgDes   = self.get_argument('hg-des',   strip=False)

        rData = yield torncelery.async(new_hostgroup, hgName, hgDes)
        self.write(rData)
class NewProject(BaseHandler, object):
    @coroutine
    def post(self, *args, **kwargs):
        repo        = self.get_argument('repo',     strip=False)
        alias       = self.get_argument('alias',    strip=False)
        webapp      = self.get_argument('webapp',   strip=False)
        reliable    = 1 if self.get_argument('reliable', default=0,strip=False) else 0
        rely_id     = self.get_argument('rely_id',  strip=False)

        rData = yield torncelery.async(new_project, repo, alias, webapp, reliable, rely_id)
        self.write(rData)

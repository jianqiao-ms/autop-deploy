#!/usr/bin/env python2
# -*- coding:UTF-8 -*-

# 系统包
from __future__ import print_function
from __future__ import absolute_import
from tornado.gen import coroutine
import json

# 三方包
import torncelery

# 自定义包
from ._handler import BaseHandler

from proj.db import mysql_insert
from proj.db import mysql_delete
from proj.db import mysql_update
from proj.db import mysql_query
from proj.db import mysql_get

from proj.tasks_ucd import auto_deploy
from proj.tasks_new import new_autorule
from proj.tasks_del import del_autorule

class Deploy(BaseHandler, object):
    @coroutine
    def get(self, module = ''):
        data = dict()
        if len(module):
            data['rules']   = yield torncelery.async(mysql_query,
                                                "SELECT \
                                                    P.`name`                AS PName, \
                                                    IFNULL(H.`ip_addr`,HG.`name`) AS Container, \
                                                    AR.`token`               AS ARToken, \
                                                    AR.`id`                  AS ARId \
                                                FROM \
                                                    `t_deploy_auto_rule` AS AR \
                                                LEFT JOIN `t_assets_project` AS P ON AR.`proj_id` = P.`id` \
                                                LEFT JOIN `t_assets_hostgroup` AS HG ON AR.`hg_id` = HG.`id` AND AR.`hg_id` IS NOT NULL \
                                                LEFT JOIN `t_assets_host` AS H ON AR.`host_id` = H.`id` AND AR.`host_id` IS NOT NULL ")
            data['host']    = yield torncelery.async(mysql_query,
                                                  "SELECT "
                                                  "* "
                                                  "FROM `t_assets_host` AS H "
                                                  "WHERE H.`hg_id`=''")
            data['hg']      = yield torncelery.async(mysql_query,
                                                  "SELECT "
                                                  "* "
                                                  "FROM `t_assets_hostgroup`")
            data['proj'] = yield torncelery.async(mysql_query,
                                                "SELECT "
                                                "* "
                                                "FROM `t_assets_project`")
            self.render("deploy-{}.html".format(module), data = data)
            return
        self.render('deploy.html')


class Auto(BaseHandler, object):
    @coroutine
    def post(self, *args, **kwargs):
        token       = kwargs['token']
        req_body    = json.loads(self.request.body)
        before      = req_body['before']
        after       = req_body['after']
        push_branch = req_body['ref'].split('/')[2]

        rData = yield torncelery.async(auto_deploy, token, push_branch, before, after)
        print(rData)
        self.write('OK')

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
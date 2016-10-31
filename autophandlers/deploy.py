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

from proj.tasks_ucd import auto_deploy

class Deploy(BaseHandler, object):
    @coroutine
    def get(self, module = ''):
        data = dict()
        if len(module):
            data['env']     = yield torncelery.async(mysql_get, 'SELECT * FROM `t_assets_env`')
            data['rules']   = yield torncelery.async(mysql_get,
                                                "SELECT \
                                                    P.`name`                AS PName, \
                                                    ENV.`name`              AS EName,\
                                                    IFNULL(H.`ip_addr`,HG.`name`) AS Container, \
                                                    AR.`token`               AS ARToken, \
                                                    AR.`id`                  AS ARId \
                                                FROM \
                                                    `t_deploy_auto_rule` AS AR \
                                                LEFT JOIN `t_assets_project` AS P ON AR.`project_id` = P.`id` \
                                                LEFT JOIN `t_assets_hostgroup` AS HG ON AR.`hg_id` = HG.`id` AND AR.`hg_id` IS NOT NULL \
                                                LEFT JOIN `t_assets_host` AS H ON AR.`host_id` = H.`id` AND AR.`host_id` IS NOT NULL \
                                                LEFT JOIN `t_assets_env` AS ENV ON ENV.`id` = HG.`env_id` \
                                                OR ENV.id = H.env_id")
            data['host']    = yield torncelery.async(mysql_get,
                                                  "SELECT "
                                                  "* "
                                                  "FROM `t_assets_host` AS H "
                                                  "WHERE H.`group_id`=''")
            data['hg']      = yield torncelery.async(mysql_get,
                                                  "SELECT "
                                                  "* "
                                                  "FROM `t_assets_hostgroup`")
            data['proj'] = yield torncelery.async(mysql_get,
                                                "SELECT "
                                                "* "
                                                "FROM `t_assets_project`")
            self.render("deploy-{}.html".format(module), data = data)
            return
        self.render('deploy.html')


class Auto(RequestHandler, object):
    @coroutine
    def post(self, *args, **kwargs):
        token = kwargs['token']
        rbody = json.loads(self.request.body)
        before = rbody['before']
        after = rbody['after']

        # print self.request.body

        rData = yield torncelery.async(auto_deploy, token, before, after)
        # self.write(rData)
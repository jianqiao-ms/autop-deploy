#!/usr/bin/env python2.7
# -*- coding:utf-8 -*-

import os
import json
import traceback
import time
import datetime
import subprocess

import tornado.ioloop
import tornado.options
from tornado.websocket import WebSocketHandler
from tornado.web import RequestHandler
from tornado.web import Application
from tornado.web import asynchronous
from tornado.gen import coroutine
import torncelery

from tasks import mysql_query
from tasks import mysql_get
from tasks import deploy
from tasks import new_host

# 自定义方法，格式化返回数据
class DateJsonEncoder(json.JSONEncoder, object):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.__str__()
        if isinstance(obj, datetime.date):
            return obj.__str__()
        else:
            return json.JSONEncoder.default(self, obj)

def fdumps(obj, status_code, request_method):
    if status_code >= 200 and status_code < 400:
        obj['status'] = 'OK'
    else:
        obj['status'] = 'ERROR'
    obj['status_code'] = status_code
    obj['request_method'] = request_method
    return json.dumps(obj, indent=4, cls=DateJsonEncoder)

# 自定义方法
def getLocaltime():
    return time.strftime("%Y-%m-%d %H:%M:%S")

# websockets connections
liveWebSockets = set()
def webSocketSendMessage(message):
    removable = set()
    for ws in liveWebSockets:
        if not ws.ws_connection or not ws.ws_connection.stream.socket:
            removable.add(ws)
        else:
            ws.write_message(message)
    for ws in removable:
        liveWebSockets.remove(ws)

# 返回tornad app对象
settings = dict(
    debug           = True,
    gzip            = True,
    template_path   = os.path.join(os.path.dirname(__file__), "templates"),
    static_path     = os.path.join(os.path.dirname(__file__), "static"),
)
def make_app():
    return Application([
        (r'/', Index),
        (r'/websocket',MsgSocket),
        (r'/admin', Admin),
        (r'/admin/?(?P<module>[a-z]+)', Admin),
        (r"/deploy", Deploy),
        (r"/deploy/?(?P<module>[a-z]+)", Deploy),

        (r'/new/host', NewHost)
    ], **settings)

class curlRequestHandler(RequestHandler, object):
    def getReturn(self, text ,code = 200):
        if self.request.headers['User-Agent'] == 'autop':
            if code != 200:
                self.set_status(404)
            self.write(text)
        else:
            if code != 200:
                self.set_status(404)
            self.write('<pre>{text}<pre>'.format(text = text))

class Index(RequestHandler, object):
    def get(self):
        self.render("index.html")

class MsgSocket(WebSocketHandler, object):
    def check_origin(self, origin):
        return True

    def open(self):
        liveWebSockets.add(self)
        print("WebSocket opened")

    def on_message(self, message):
        self.write_message(u"You said: " + message)

    def on_close(self):
        print("WebSocket closed")

class Deploy(curlRequestHandler, object):
    @coroutine
    def get(self, module = ''):
        if len(module):
            self.render("deploy-{}.html".format(module))
        self.render('deploy.html')

class Admin(RequestHandler, object):
    @coroutine
    def get(self, module=''):
        main_content_sql = dict(
                               host        = "SELECT "
                                                "H.`id`                          AS HId,"
                                                "H.`alias`                       AS HAlias,"
                                                "H.`ip_addr`                     AS HIp,"
                                                "IFNULL(ENV.`name`,'')           AS EName,"
                                                "HType.`name`                    AS HTypeName,"
                                                "IFNULL(HG.`id`,'')              AS HGroupId,"
                                                "IFNULL(HG.`name`,'')            AS HGName "
                                              "FROM `t_assets_host`              AS H "
                                              "LEFT JOIN `t_assets_hostgroup`    AS HG "
                                              "ON H.`group_id` = HG.`id` "
                                              "LEFT JOIN `t_assets_env`          AS ENV "
                                              "ON ENV.`id`=H.`id` "
                                              "LEFT JOIN `t_assets_hosttype`     AS HType "
                                              "ON HType.`id`=H.`type_id`",
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
                                                 'alias                          AS PAlias '
                                               'FROM `t_assets_project`')

        if len(module):
            data = dict()

            main_content = yield torncelery.async(mysql_get, main_content_sql[module])
            data['main_content'] = main_content

            if module=='host':
                data['env'] = yield torncelery.async(mysql_get, 'SELECT * FROM `t_assets_env`')
                data['hosttype'] = yield torncelery.async(mysql_get, 'SELECT * FROM `t_assets_hosttype`')
                data['hostgroup'] = yield torncelery.async(mysql_get, 'SELECT * FROM `t_assets_hostgroup`')

            if module == 'hostgroup':
                data['env'] = yield torncelery.async(mysql_get, 'SELECT * FROM `t_assets_env`')

            self.render("admin-{}.html".format(module),data = data)
            return
        self.render('admin.html')
class NewHost(RequestHandler, object):
    @coroutine
    def post(self, *args, **kwargs):
        envId   = self.get_argument('env')
        ipaddr  = self.get_argument('ipaddr')
        hgId    = self.get_argument('hostgroup')
        uName   = self.get_argument('username')
        uPwd    = self.get_argument('password')

        if uPwd==' ':
            print '空格'

        rData = yield torncelery.async(new_host, envId, ipaddr, hgId, uName, uPwd)
        self.write(rData)

if __name__ == "__main__":
    print 'Starting Server...'
    tornado.options.parse_command_line()
    app = make_app()
    app.listen(8888)
    tornado.ioloop.IOLoop.instance().start()
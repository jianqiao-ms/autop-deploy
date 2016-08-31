#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os
import json
import traceback
import time
import datetime

import tornado.ioloop
from tornado.web import RequestHandler
from tornado.web import Application
import tornado.options
from tornado.gen import coroutine

from tasks import mysql_query

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

# 返回tornad app对象
settings = dict(
    debug           = True,
    gzip            =  True,
    template_path   = os.path.join(os.path.dirname(__file__), "templates"),
    static_path     = os.path.join(os.path.dirname(__file__), "static"),
)

def make_app():
    return Application([
        (r"/", Index),
        (r"^/assets", Assets),
        (r"^/assets/([a-zA-Z]+)", Assets)
    ], **settings)

class Index(RequestHandler, object):
    def get(self):
        self.render("base.html")

class Assets(RequestHandler, object):
    @coroutine
    def get(self, item=''):

        item_table = dict(host      = "t_assets_host",
                          hosttype  = "t_assets_hosttype",
                          hostgroup = "t_assets_hostgroup",
                          env       = "t_assets_env",
                          project   = "t_assets_project")

        if not item:
            print 'r'
            self.render("assets.html",result = '')
        else:
            result = mysql_query("SELECT * FROM {table_name}".format(table_name=item_table[item]))
            self.render("assets.html", result = result)

if __name__ == "__main__":
    tornado.options.parse_command_line()
    app = make_app()
    app.listen(8888)
    tornado.ioloop.IOLoop.instance().start()
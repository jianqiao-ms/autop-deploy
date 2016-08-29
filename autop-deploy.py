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
        # (r"^/assets"
        #     r"(?P<path0>/?)(?P<item>[A-Za-z]*)"
        #     r"(?P<path1>/?)(?P<function>[A-Za-z]*)", Assets),
        # (r"^/deploy"
        #     r"(?P<path0>/?)(?P<item>[A-Za-z-]*)"
        #     r"(?P<path1>/?)(?P<function>[A-Za-z]*)", Deploy),
    ], **settings)

class Index(RequestHandler, object):
    def get(self):
        a = mysql_query("SELECT * FROM `t_deploy_task`")
        print a
        # self.write(json.dumps(a, cls=DateJsonEncoder))
        self.write(a)

if __name__ == "__main__":
    tornado.options.parse_command_line()
    app = make_app()
    app.listen(8888)
    tornado.ioloop.IOLoop.instance().start()
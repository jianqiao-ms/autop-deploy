#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os
import json
import traceback
import time
import datetime
import subprocess

import tornado.ioloop
import tornado.options
from tornado.web import RequestHandler
from tornado.web import Application
from tornado.web import asynchronous
from tornado.gen import coroutine
import torncelery

from tasks import mysql_query
from tasks import mysql_get
from tasks import deploy

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
        # (r"^/deploy", Deploy),
        (r"^/deploy/([0-9]+)", Deploy)
    ], **settings)


class curlRequestHandler(RequestHandler, object):
    def getReturn(self, text):
        if self.request.headers['User-Agent'] == 'autop':
            self.write(text)
        else:
            self.write('<pre>{text}<pre>'.format(text = text))


class Index(RequestHandler, object):
    def get(self):
        # self.write('a\nb')
        self.render("base.html")


class Deploy(curlRequestHandler, object):
    @coroutine
    def get(self, pid = ''):
        pname = mysql_get("SELECT `name` FROM `t_assets_project` WHERE `id`={pid}".format(pid = pid))[0]['name']
        result = yield torncelery.async(deploy, pname)

        self.getReturn('\n'.join(result['msg']))

if __name__ == "__main__":
    print 'Starting Server...'
    tornado.options.parse_command_line()
    app = make_app()
    app.listen(8888)
    tornado.ioloop.IOLoop.instance().start()
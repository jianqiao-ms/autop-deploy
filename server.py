#!/usr/bin/env python2
# -*- coding:UTF-8 -*-

import os

import tornado.ioloop
import tornado.options
from tornado.web import RequestHandler
from tornado.web import Application

from autophandlers import index
from autophandlers import admin
from autophandlers import deploy


# 返回tornad app对象
settings = dict(
    debug           = True,
    gzip            = True,
    template_path   = os.path.join(os.path.dirname(__file__), "templates"),
    static_path     = os.path.join(os.path.dirname(__file__), "static"),
)

def make_app():
    return Application([
        (r'/', index.Index),
        (r'/admin', admin.Admin),
        (r'/admin/?(?P<module>[a-z]+)', admin.Admin),
        (r"/deploy", deploy.Deploy),
        (r"/deploy/?(?P<module>[a-z]+)", deploy.Deploy),

        (r'/new/host', admin.NewHost),
        (r'/new/hostgroup', admin.NewHostgroup),
        (r'/new/project', admin.NewProject),
        (r'/new/autorule', admin.NewAutoRule),
        (r'/auto/(?P<token>.+)', deploy.Auto),

        (r'/del/autorule',admin.DelAutoRule)
    ], **settings)

if __name__ == "__main__":
    print('Starting Server...')
    tornado.options.parse_command_line()
    app = make_app()
    app.listen(8888)
    tornado.ioloop.IOLoop.instance().start()
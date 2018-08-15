#! /usr/bin/env python
#-* coding: utf-8 -*

# Official packages
import os, sys
import io, json

# 3rd-party Packages
import tornado.web

# Local Packages
from handler.index import IndexHandler


# CONST

# Class&Function Defination
# class IndexHandler(tornado.web.RequestHandler):
#     def get(self, *args, **kwargs):
#         self.render('index.html')


# Logic
if __name__ == '__main__':
    settings = {
        'login_url': '/login',
        'template_path': os.path.join(os.path.dirname(__file__), "template")
    }

    from tornado.options import parse_command_line
    from tornado.web import Application
    from tornado.ioloop import IOLoop

    parse_command_line()
    application = Application([
        '/',
    ], **settings)
    application.listen(60000)
    IOLoop.current().start()

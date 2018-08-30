#! /usr/bin/env python
#-* coding: utf-8 -*

# Official packages
import os

# 3rd-party Packages
import tornado.options
from tornado.ioloop import IOLoop

# Local Packages
from classes.appliacation import Application

from handler.index import IndexHandler
from handler.upload import UploadHandler
from handler.database import DatabaseHandler

# CONST

# Class&Function Defination

# Logic
if __name__ == '__main__':
    settings = {
        'login_url': '/login',
        'template_path': os.path.join(os.path.dirname(__file__), "template"),
        "static_path": os.path.join(os.path.dirname(__file__), "static"),
    }

    tornado.options.options.logging = None
    tornado.options.parse_command_line()
    application = Application([
        ('/', IndexHandler),
        ('/upload', UploadHandler),
        ('/(?P<object>.+)\/*(?P<id>.*)', DatabaseHandler),
    ], **settings)

    application.listen(60000)
    IOLoop.current().start()
#! /usr/bin/env python
#-* coding: utf-8 -*

# Official packages
import os

# 3rd-party Packages
import tornado.options
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop

# Local Packages
from classes.appliacation import Application

from handler.index import IndexHandler

from handler.inventory import InventoryHandler

from handler.upload import UploadHandler
from handler.database import DatabaseHandler

# CONST
settings = {
        'login_url': '/login',
        'template_path': os.path.join(os.path.dirname(__file__), "template"),
        "static_path": os.path.join(os.path.dirname(__file__), "static"),
        "debug":True
    }

# Class&Function Defination
application = Application([
        ('/', IndexHandler),
        ('/inventory/(?P<item>.+)', InventoryHandler),
        ('/upload', UploadHandler),
        ('/(?P<object>.+)\/*(?P<id>.*)', DatabaseHandler),
    ], **settings)

# Logic
if __name__ == '__main__':
    tornado.options.options.logging = None
    tornado.options.parse_command_line()
    # server = HTTPServer(application)
    application.listen(60000)
    IOLoop.current().start()
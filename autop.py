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

# CONST
# 程序运行logger


# Class&Function Defination
# Logic
if __name__ == '__main__':
    settings = {
        'login_url': '/login',
        'template_path': os.path.join(os.path.dirname(__file__), "template"),
        "static_path": os.path.join(os.path.dirname(__file__), "static"),
    }

    tornado.options.parse_command_line()
    application = Application([
        ('/', IndexHandler),
        ('/upload', UploadHandler),
    ], **settings)

    application.listen(60000, max_body_size=20 * 1024 * 1024 * 1024)
    IOLoop.current().start()

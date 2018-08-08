#! /usr/bin/env python
#-* coding: utf-8 -*

# Official packages
import os, sys
import io, json

# 3rd-party Packages
import tornado.web

# Local Packages

# CONST
plugins = next(os.walk(os.path.join(os.path.dirname(__file__), "plugins")))[1]



# Class&Function Defination

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
    application = Application(url_map, **settings)
    application.listen(60000)
    IOLoop.current().start()

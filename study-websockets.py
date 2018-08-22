#! /usr/bin/env python
#-* coding: utf-8 -*

# Official packages

# 3rd-party Packages
import tornado.web
from tornado.options import parse_command_line
from tornado.web import Application
from tornado.ioloop import IOLoop

# Local Packages

# CONST

# Class&Function Defination
class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Hello, world")

def make_app():
    return tornado.web.Application([
        (r"/", MainHandler),
    ])

# Logic
if __name__ == "__main__":
    parse_command_line()
    app = make_app()
    app.listen(8888)
    IOLoop.current().start()

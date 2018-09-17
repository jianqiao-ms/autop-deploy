#! /usr/bin/env python
#-* coding: utf-8 -*

# Official packages
import os

# 3rd-party Packages
import tornado.options
from tornado.routing import RuleRouter, Rule, PathMatches
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop


# Local Packages
from classes.appliacation import Application

from handler.index import IndexHandler

from handler.inventory import app_inventory

from handler.upload import UploadHandler
from handler.database import DatabaseHandler

# CONST


# Class&Function Defination
app_base = Application([
        ('/', IndexHandler),
])

router = RuleRouter([
    Rule(PathMatches("/inventory.*"), app_inventory),
    Rule(PathMatches("/.*"), app_base)
])


# Logic
if __name__ == '__main__':
    tornado.options.options.logging = None
    tornado.options.parse_command_line()
    server = HTTPServer(router)
    server.listen(60000)
    IOLoop.current().start()
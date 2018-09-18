#! /usr/bin/env python
#-* coding: utf-8 -*

# Official packages

# 3rd-party Packages
import tornado.options
from tornado.routing import RuleRouter, Rule, PathMatches
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop

# Local Packages
from handler.dashboard import app_dashboard
from handler.inventory import app_inventory

# CONST


# Class&Function Defination
router = RuleRouter([
    Rule(PathMatches("/inventory.*"), app_inventory),
    Rule(PathMatches("/.*"), app_dashboard)
])

# Logic
if __name__ == '__main__':
    tornado.options.options.logging = None
    tornado.options.parse_command_line()
    server = HTTPServer(router)
    server.listen(60000)
    IOLoop.current().start()
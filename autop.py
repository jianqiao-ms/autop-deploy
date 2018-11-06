#! /usr/bin/env python
#-* coding: utf-8 -*

# Official packages

# 3rd-party Packages
import tornado.options
from tornado.routing import RuleRouter, Rule, PathMatches
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop

# Local Packages
from classes.appliacation import Application
from handler.gitlab import app_api
from handler.dashboard import app_dashboard
from handler.assets import app_inventory
from handler.deploy import app_deploy
import handler.api.IO.Route as IORoute

# CONST


# Class&Function Defination
router_rules = list()
# router_rules.extend(app_api)
# router_rules.extend(app_dashboard)
# router_rules.extend(app_inventory)
# router_rules.extend(app_deploy)
router_rules.extend(IORoute.route)

# Logic
if __name__ == '__main__':
    tornado.options.options.logging = None
    tornado.options.parse_command_line()
    server = HTTPServer(Application(router_rules))
    server.listen(60000)
    IOLoop.current().start()
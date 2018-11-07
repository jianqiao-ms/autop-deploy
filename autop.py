#! /usr/bin/env python
#-* coding: utf-8 -*

# Official packages

# 3rd-party Packages
import tornado.options
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop

# Local Packages
from classes.appliacation import Application
from handler.dashboard import route as IndexRoute
from handler.api.Inventory.Route import route as IORoute
from handler.view.Inventory.Route import route as InventoryRoute

# CONST


# Class&Function Defination
router_rules = list()
router_rules.extend(IndexRoute)
router_rules.extend(IORoute)
router_rules.extend(InventoryRoute)

# Logic
if __name__ == '__main__':
    tornado.options.options.logging = None
    tornado.options.parse_command_line()
    server = HTTPServer(Application(router_rules))
    # server = HTTPServer(application)
    server.listen(60000)
    IOLoop.current().start()

#! /usr/bin/env python
#-* coding: utf-8 -*

# Official packages

# 3rd-party Packages
import tornado.options
from tornado.ioloop import IOLoop

# Local Packages
from classes import Application
from handler import route
# CONST


# Class&Function Defination
ROUTE = list()
ROUTE.extend(route)


# Logic
if __name__ == '__main__':

    application = Application(
        ROUTE
    )
    application.listen(60000)
    IOLoop.current().start()

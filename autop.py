#! /usr/bin/env python
#-* coding: utf-8 -*

# Official packages
import asyncio
# 3rd-party Packages
import tornado.platform.asyncio
import tornado.options
from tornado.ioloop import IOLoop

# Local Packages
from classes import ConfigManager
from classes import LogManager
from classes import Application
from handler import route

# CONST

# Class&Function Defination
ROUTE = list()
ROUTE.extend(route)


# Logic
if __name__ == '__main__':
    tornado.platform.asyncio.AsyncIOMainLoop().install()
    IOLoop = asyncio.get_event_loop()
    
    cm = ConfigManager()
    lm = LogManager()

    lm.get_base_logger()
    configuration = cm.get_config()
    configuration.validate()
    lm.get_logger(configuration.log)

    application = Application(
        ROUTE,
    configuration = configuration)
    application.listen(60000)
    IOLoop.run_forever()
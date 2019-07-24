#! /usr/bin/env python
#-* coding: utf-8 -*

# Official packages

# 3rd-party Packages
from tornado.platform import asyncio

# Local Packages
from api.classes import Application
from api.handler import route


# CONST

# Class&Function Defination

# Logic
if __name__ == '__main__':
    IOLoop = asyncio.IOLoop()
    
    # cm = ConfigManager()
    # lm = LogManager()

    # lm.get_base_logger()
    # configuration = cm.get_config()
    # configuration.validate()
    # lm.get_logger(configuration.log)
    #
    application = Application(route)
    application.listen(8080)
    IOLoop.current().start()
#! /usr/bin/env python
#-* coding: utf-8 -*

# Official packages

# 3rd-party Packages
from tornado.platform import asyncio
from tornado.options import parse_command_line
from tornado.web import Application
# Local Packages
from api.handler import route


# CONST

# Class&Function Defination

# Logic
if __name__ == '__main__':
    parse_command_line()
    settings = {'debug': True}

    IOLoop = asyncio.IOLoop()
    
    # cm = ConfigManager()
    # lm = LogManager()

    # lm.get_base_logger()
    # configuration = cm.get_config()
    # configuration.validate()
    # lm.get_logger(configuration.log)
    #
    application = Application(route, **settings)
    application.listen(8080)
    IOLoop.current().start()
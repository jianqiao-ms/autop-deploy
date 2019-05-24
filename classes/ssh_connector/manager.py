#! /usr/bin/env python
#-* coding: utf-8 -*

# Official packages
import os
import logging
import json
import secrets
import hashlib

# 3rd-party Packages
from tornado.ioloop import IOLoop
from tornado.web import stream_request_body
from tornado.web import HTTPError

# Local Packages
from classes import UIRequestHandler

# CONST

# Class&Function Defination
class SSHPtyManager():
    def __init__(self, extra_env=None, ioloop=None):
        if ioloop is not None:
            self.ioloop = ioloop
        else:
            import tornado.ioloop
            self.ioloop = IOLoop.instance()

# Logic
if __name__ == '__main__':
    
    from tornado.web import Application
    import tornado.options

    tornado.options.options.logging = None
    tornado.options.parse_command_line()
    application = Application([
        (r"/api/v1/gitlab/jobscripts", ),
    ])
    application.listen(60000)
    IOLoop.current().start()
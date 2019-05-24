#! /usr/bin/env python
#-* coding: utf-8 -*

# Official packages
import os
import logging
import json
import secrets
import hashlib

# 3rd-party Packages
from tornado.web import stream_request_body
from tornado.web import HTTPError

# Local Packages
from classes import UIRequestHandler

# CONST

# Class&Function Defination


# Logic
if __name__ == '__main__':
    from tornado.ioloop import IOLoop
    from tornado.web import Application
    import tornado.options

    tornado.options.options.logging = None
    tornado.options.parse_command_line()
    application = Application([
        (r"/api/v1/gitlab/jobscripts", ),
    ])
    application.listen(60000)
    IOLoop.current().start()
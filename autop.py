#! /usr/bin/env python
#-* coding: utf-8 -*

# Official packages
import os, sys
import io, json
import logging

# 3rd-party Packages
import tornado.web
from tornado.options import parse_command_line
from tornado.web import Application
from tornado.ioloop import IOLoop

# Local Packages
from handler.index import IndexHandler

# CONST
# 程序运行logger
logger = logging.getLogger()
logger.setLevel(logging.INFO)

console_logger = logging.StreamHandler()
console_logger.setLevel(logging.DEBUG)
console_fmt = logging.Formatter('[%(asctime)s] %(levelname)-7s [%(funcName)s: %(filename)s]%(lineno)d -- %(message)s')
console_logger.setFormatter(console_fmt)

file_logger = logging.FileHandler('autop.log')
file_logger.setLevel(logging.INFO)
file_fmt = logging.Formatter('[%(asctime)s] %(levelname)-7s [%(funcName)s: %(filename)s]%(lineno)d -- %(message)s')
file_logger.setFormatter(file_fmt)

logger.addHandler(console_logger)
logger.addHandler(file_logger)


# Class&Function Defination

# Logic
if __name__ == '__main__':
    settings = {
        'login_url': '/login',
        'template_path': os.path.join(os.path.dirname(__file__), "template")
    }

    parse_command_line()
    application = Application([
        ('/', IndexHandler),
    ], **settings)

    application.listen(60000)
    IOLoop.current().start()

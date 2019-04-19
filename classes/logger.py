#! /usr/bin/env python
#-* coding: utf-8 -*

__all__ = ['log', 'access_log', 'app_log', 'gen_log']

# Official packages
import os
import json
import logging
from logging.handlers import TimedRotatingFileHandler

# 3rd-party Packages
import tornado.log

# Local Packages

# CONST
CONFIG_FILE = os.path.join(os.path.abspath(os.path.join(__file__, os.pardir, os.pardir)), 'conf/log.json')
with open(CONFIG_FILE, 'r') as fp:
    configuration = json.load(fp)
access_log  = tornado.log.access_log
app_log     = tornado.log.app_log
access_log.setLevel(logging._nameToLevel[configuration['level'].upper()])
app_log.setLevel(logging._nameToLevel[configuration['level'].upper()])


# Class&Function Defination
def getHandler(cls:callable, filename='autop.log',
               formatString='[%(asctime)s] %(levelname)s %(filename)s %(funcName)s %(lineno)d -- %(message)s'):

    handler = cls() if logging.StreamHandler == cls else \
        cls(filename = os.path.join(configuration['path'], filename), when='D')
    handler.setFormatter(logging.Formatter(formatString))
    return handler

# Logic
access_log.addHandler(
    getHandler(TimedRotatingFileHandler, filename='access.log', formatString = '[%(asctime)s] %(message)s'))
app_log.addHandler(getHandler(TimedRotatingFileHandler, filename='autop.log', formatString = configuration['format']))
if configuration['console']:
    access_log.addHandler(getHandler(logging.StreamHandler, formatString = '[%(asctime)s] %(message)s'))
    app_log.addHandler(getHandler(logging.StreamHandler, formatString = configuration['format']))
gen_log     = tornado.log.gen_log
map(gen_log.addHandler, app_log.handlers)
log = app_log

if __name__ == '__main__':
    import time
    log.debug(time.strftime("%Y-%m-%d %H:%M:%S"))

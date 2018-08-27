#! /usr/bin/env python
#-* coding: utf-8 -*

# Official packages
import os
import json
import logging
import logging.config

# 3rd-party Packages
from tornado.log import access_log

# Local Packages

# CONST
CONFIG_FILE = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'conf/logging.json')
with open(CONFIG_FILE, 'r') as file:
    config = json.load(file)

logger = logging.getLogger()
logging.config.dictConfig(config)

# Class&Function Defination

# Logic
if __name__ == '__main__':
    print(access_log.handlers)
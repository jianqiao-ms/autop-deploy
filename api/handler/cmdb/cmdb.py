#! /usr/bin/env python
# -* coding: utf-8 -*

# Official packages
import logging
import json
import sys
import traceback

# 3rd-party Packages

# Local Packages
from api.classes import RESTRequestHandler
from api.classes.databases import *

# CONST

# Class&Function Defination
class CMDBLabelHandler(RESTRequestHandler):
    def get(self):
        get_columns(Device)
        # logging.info(get_columns(Label))


# Logic
if __name__ == '__main__':
    pass
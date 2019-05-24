#! /usr/bin/env python
#-* coding: utf-8 -*

# Official packages
import os.path
import logging
import json

# 3rd-party Packages

# Local Packages
from classes.req_handler import UIRequestHandler

# CONST

# Class&Function Defination
class SSHConnectorViewHandler(UIRequestHandler):
    """
    ssh_connector UI
    """

    def get(self):
        self.render("ssh_connector/ui.html")

    
# Logic
if __name__ == '__main__':
    pass

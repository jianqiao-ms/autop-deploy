#! /usr/bin/env python
#-* coding: utf-8 -*

# Official packages
import os.path
import json

# 3rd-party Packages
# Local Packages
from classes.application import LOGGER
from classes.handlers import NotInitialized
from classes.handlers import RequestHandler
from classes.handlers import ViewRequestHandler

# CONST

# Class&Function Defination
class InventoryViewHandler(ViewRequestHandler):
    """
    Inventory展示页面Handler
    """
    __route_module__ =  "inventory"
    def get(self):
        if "action" in self.__arguments_dict__ and self.__arguments_dict__["action"] == "new":
            self.render(self.__template_new__)
        else:
            self.render(self.__template__)

class DashboardInventoryViewHandler(InventoryViewHandler):
    __route_item__ = "dashboard"

class DistrictInventoryViewHandler(InventoryViewHandler):
    __route_item__ = "district"

class HostInventoryViewHandler(InventoryViewHandler):
    __route_item__ = "host"

class HostgroupInventoryViewHandler(InventoryViewHandler):
    __route_item__ = "hostgroup"

class ProjectInventoryViewHandler(InventoryViewHandler):
    __route_item__ = "project"

# Logic
if __name__ == '__main__':
    pass

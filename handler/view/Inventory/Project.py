#! /usr/bin/env python
# -* coding: utf-8 -*

# Official packages

# 3rd-party Packages

# Local Packages
from classes.schema.SchemaInventory import SchemaProject
from .Inventory import InventoryViewHandler


# CONST

# Class&Function Defination
class ProjectInventoryViewHandler(InventoryViewHandler):
    __route_path__ = "project"

    def get_pre(self):
        return list(filter(
            lambda x:x.gitlab_id,
            self.__records_json__
        ))

    @property
    def __schema__(self):
        return SchemaProject


# Logic
if __name__ == '__main__':
    pass

#! /usr/bin/env python
# -* coding: utf-8 -*

# Official packages

# 3rd-party Packages

# Local Packages
from classes.database.SchemaInventory import SchemaHost
from .Inventory import InventoryViewHandler


# CONST

# Class&Function Defination
class HostInventoryViewHandler(InventoryViewHandler):
    __route_path__ = "host"

    @property
    def __schema__(self):
        return SchemaHost


# Logic
if __name__ == '__main__':
    pass

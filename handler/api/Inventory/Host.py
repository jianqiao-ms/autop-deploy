#! /usr/bin/env python
# -* coding: utf-8 -*

# Official packages

# 3rd-party Packages

# Local Packages
from classes.database.SchemaInventory import SchemaHost
from ._base import InventoryApiHandler


# CONST

# Class&Function Defination
class HostInventoryApiHandler(InventoryApiHandler):
    __route_path__ = "host"

    @property
    def __schema__(self):
        return SchemaHost


# Logic
if __name__ == '__main__':
    pass

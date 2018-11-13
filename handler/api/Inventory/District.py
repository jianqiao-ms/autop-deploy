#! /usr/bin/env python
#-* coding: utf-8 -*

# Official packages

# 3rd-party Packages

# Local Packages
from classes.schema.SchemaInventory import SchemaDistrict
from ._base import InventoryApiHandler

# CONST

# Class&Function Defination
class DistrictInventoryApiHandler(InventoryApiHandler):
    __route_path__ = "district"

    @property
    def __schema__(self):
        return SchemaDistrict

# Logic
if __name__ == '__main__':
    pass

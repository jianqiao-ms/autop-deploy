#! /usr/bin/env python
#-* coding: utf-8 -*

# Official packages

# 3rd-party Packages

# Local Packages
from classes.schema.SchemaInventory import SchemaDistrict
from ._base import InventoryViewHandler
# CONST

# Class&Function Defination
class DistrictInventoryViewHandler(InventoryViewHandler):
    __route_path__ = "district"
    @property
    def __schema__(self):
        return SchemaDistrict

    

# Logic
if __name__ == '__main__':
    pass

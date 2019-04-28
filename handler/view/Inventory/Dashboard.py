#! /usr/bin/env python
#-* coding: utf-8 -*

# Official packages

# 3rd-party Packages

# Local Packages
from classes.database.SchemaInventory import SchemaDistrict
from .Inventory import InventoryViewHandler
# CONST

# Class&Function Defination
class DashboardInventoryViewHandler(InventoryViewHandler):
    def get_pre(self):
        return None

    

# Logic
if __name__ == '__main__':
    pass
